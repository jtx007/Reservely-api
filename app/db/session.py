from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings  # fix: import the correct symbol

settings = Settings()  # type: ignore[call-arg] # DATABASE_URL loaded from env/.env file by BaseSettings

engine = create_engine(settings.sqlalchemy_database_url)  # use correct property name, lowercase

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
