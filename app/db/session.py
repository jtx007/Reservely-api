from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.sqlalchemy_database_url)  # use correct property name, lowercase

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
