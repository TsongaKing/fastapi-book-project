from pydantic import Field, RedisDsn, PostgresDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    # Required Core Settings
    PROJECT_NAME: str = "FastAPI Book Service"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = Field(
        default="changeme-in-production",
        min_length=32,
        description="Secret key for cryptographic operations"
    )
    
    # Environment Configuration
    DEBUG: bool = False
    ENVIRONMENT: str = Field(
        default="production",
        pattern="^(development|staging|production)$"
    )

    # API Configuration
    API_PREFIX: str = "/api/v1"
    API_DOCS_URL: Optional[str] = "/docs"
    API_REDOC_URL: Optional[str] = "/redoc"

    # Database Configuration
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://user:pass@localhost:5432/dbname",
        examples=["postgresql+asyncpg://user:password@localhost:5432/database"]
    )

    # Security Configuration
    CORS_ORIGINS: List[str] = Field(
        default=[],
        description="Comma-separated list of allowed origins"
    )
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]
    CORS_HEADERS: List[str] = ["*"]

    # Redis Configuration (optional)
    REDIS_URL: Optional[RedisDsn] = None

    # Celery Configuration (optional)
    CELERY_BROKER_URL: Optional[AmqpDsn] = None

    # Model Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()