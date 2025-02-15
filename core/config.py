from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CORS_ORIGINS: list[str] = ["*"]
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Book Service"
    PROJECT_VERSION: str = "1.0.0"

settings = Settings()