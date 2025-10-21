from typing import Annotated
from urllib.parse import urlparse
import sys
from dotenv import load_dotenv
import os
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers import user, restaurant  # Your custom routers

# Database setup
db_url = os.getenv("DATABASE_URL")
if db_url is None:
    raise ValueError("DATABASE_URL must be set in the environment variables.")

# Handle SQLite vs others
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(db_url, connect_args=connect_args)
else:
    engine = create_engine(db_url)

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # You can add shutdown cleanup here if needed

# FastAPI app instance
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],   # Allows all methods
    allow_headers=["*"],   # Allows all headers
)

# Include routers
app.include_router(user.router)
app.include_router(restaurant.router)
