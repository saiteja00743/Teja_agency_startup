from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Teja Labs"
    APP_ENV: str = "development"
    SECRET_KEY: str = secrets.token_hex(32)
    ADMIN_PASSWORD: str = "admin123"  # Change this in production!

    # Database
    DATABASE_URL: str = "sqlite:///./teja_agency.db"

    # Email (SMTP)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    NOTIFICATION_EMAIL: str = ""  # Email to receive lead notifications

    # CORS
    ALLOWED_ORIGINS: str = "*"

    # Rate limiting (requests per minute)
    RATE_LIMIT: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
