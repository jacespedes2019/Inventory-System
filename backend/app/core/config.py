"""
File: config.py
Description: Centralized application configuration using environment variables.
Author: Jairo Céspedes
Date: 2025-09-05

Responsibilities:
- Provide strongly-typed settings (database URL, JWT secret, algorithm, app name).
- Load environment variables with Pydantic BaseSettings.
- Make settings accessible across the application.

Notes:
- Environment variables are loaded from `.env` in local development.
- Update JWT_SECRET and DATABASE_URL for production deployments.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    APP_NAME: str = "Inventory API"
    APP_ENV: str = "dev"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_HOURS: int = 8

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()