from typing import Annotated
import sys
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, create_engine
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
import re
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


def sanitize_integrity_error(e: IntegrityError) -> str:
    msg = str(e.orig)
    
    # Grab everything after DETAIL:
    detail_part = msg.split("DETAIL:")[1].strip() if "DETAIL:" in msg else msg

    # Extract the field inside parentheses
    match = re.search(r'Key \((.*?)\)', detail_part)
    if match:
        field = match.group(1).capitalize()  # capitalize first letter
        # Remove the "Key (field)=" part, leaving only the DB message
        cleaned_msg = re.sub(r'Key \(' + re.escape(match.group(1)) + r'\)=\([^\)]*\)\s*', '', detail_part)
        return f"{field} {cleaned_msg}"
    
    # fallback
    return detail_part
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    user_friendly_msg = sanitize_integrity_error(exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": user_friendly_msg}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": request.url.path
        }
    )


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
