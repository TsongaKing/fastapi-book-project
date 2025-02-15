# api/router.py
from fastapi import APIRouter
from api.routes.books import router as books_router  # Absolute import

api_router = APIRouter()
api_router.include_router(books_router, prefix="/books")