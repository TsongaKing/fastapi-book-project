from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text
from api.router import api_router
from core.config import settings
from api.db.database import Base, create_tables, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Async context manager for database connection lifecycle"""
    try:
        # Initialize connection pool
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        # Cleanup connections
        await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None,  # Disable redoc for security
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Security headers (add separate middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Request-ID"]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Production-ready validation error handler"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Invalid request format",
            "details": exc.errors() if settings.DEBUG else None
        }
    )

app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
    tags=["Book Management"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        429: {"description": "Rate Limit Exceeded"}
    }
)

@app.get("/healthcheck", include_in_schema=False)
async def health_check():
    """Deep health check with dependency verification"""
    return {
        "status": "healthy",
        "version": settings.PROJECT_VERSION,
        "dependencies": {
            "database": await check_db_connection()
        }
    }