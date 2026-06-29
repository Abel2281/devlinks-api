from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "DevLinks API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/devlinks"
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    # JWT
    SECRET_KEY: str = "7f9b3d8e5a1c4f2d9e6b0a3c8f1d7e2b4c6a9f0d3e1b5c7a8d2f6e9c4b1a0f3"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Caching
    PROFILE_CACHE_TTL: int = 300  

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60 

    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache
def get_settings() -> Settings:
    return Settings()