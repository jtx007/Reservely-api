from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.dependency import get_db
from models.user import User
from services import user_service
from schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)