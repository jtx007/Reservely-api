from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.dependency import get_db
from services import user_service
from schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(tags=["User"])

@router.get("/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)): 
    return user_service.get_all_users(db)


@router.get("/users/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(user_id=user_id, db=db)


@router.put("/users/{user_id}", response_model=UserRead)
def update_user_by_id(user_id: int, user_update: UserUpdate , db: Session = Depends(get_db)):
    return user_service.update_user(user_id=user_id, user_update=user_update, db=db)

@router.delete("/users/{user_id}", response_model=UserRead)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return user_service.destroy_user(user_id=user_id, db=db)
    

@router.post("/users", response_model=UserRead)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user_create, db)

