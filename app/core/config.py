# config.py
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn  # Loaded from environment variables or .env file
    ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def sqlalchemy_database_url(self) -> str:
        return str(self.DATABASE_URL)

