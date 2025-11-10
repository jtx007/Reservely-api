from typing import Annotated
import re
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.database import create_db_and_tables, get_session
from app.db.seed import seed_restaurants
from app.routers import user, restaurant  # your routers

load_dotenv()

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_restaurants()
    yield

app = FastAPI(lifespan=lifespan)

# --- Error handlers ---
def sanitize_integrity_error(e: IntegrityError) -> str:
    msg = str(e.orig)
    detail_part = msg.split("DETAIL:")[1].strip() if "DETAIL:" in msg else msg
    match = re.search(r'Key \((.*?)\)', detail_part)
    if match:
        field = match.group(1).capitalize()
        cleaned_msg = re.sub(r'Key \(' + re.escape(match.group(1)) + r'\)=\([^\)]*\)\s*', '', detail_part)
        return f"{field} {cleaned_msg}"
    return detail_part

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    user_friendly_msg = sanitize_integrity_error(exc)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": user_friendly_msg})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "path": request.url.path})

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(user.router)
app.include_router(restaurant.router)
