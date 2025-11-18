# config.py
from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

# Ensure .env is loaded before creating Settings instance
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn  # Loaded from environment variables or .env file
    ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"  # JWT secret key - MUST be set in production!
    ALGORITHM: str = "HS256"  # JWT algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token expiration time in minutes

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def sqlalchemy_database_url(self) -> str:
        return str(self.DATABASE_URL)

# Create a singleton settings instance
settings = Settings()  # type: ignore[call-arg] # DATABASE_URL and SECRET_KEY loaded from env/.env file by BaseSettings

