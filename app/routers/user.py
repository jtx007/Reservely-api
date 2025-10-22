from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from db.dependency import get_db
from services import user_service
from schemas.user import UserRead, UserCreate, UserUpdate, UserLogin, Token
from core.auth import create_access_token

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

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = user_service.authenticate_user(user_login.username, user_login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

