
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