from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.dependency import get_db
from services import user_service
from schemas.user import UserRead, UserCreate

router = APIRouter(tags=["User"])

@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    
    return user_service.get_all_users(db)


@router.post("/users", response_model=UserRead)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user_create, db)