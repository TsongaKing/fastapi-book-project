from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    # Required Core Settings
    PROJECT_NAME: str = "FastAPI Book Service"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = Field(
        min_length=32,
        description="Secret key for cryptographic operations"
    )
    
    # Environment Configuration
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # API Configuration
    API_PREFIX: str = "/api/v1"
    API_DOCS_URL: Optional[str] = "/docs"

    # Database Configuration
    DATABASE_URL: PostgresDsn = "sqlite:///./books.db"

    # CORS Configuration
    CORS_ORIGINS: List[str] = []
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()