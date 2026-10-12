"""
Food Order API - Application Configuration
==========================================
Centralized configuration management loading environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
ENV_FILE: Path = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


class Settings:
    """
    Application settings container.
    Reads environment variables with sensible defaults for local development.
    """

    APP_NAME: str = os.getenv("APP_NAME", "Food Order API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./food_order.db")


settings: Settings = Settings()
