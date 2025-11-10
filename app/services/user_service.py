
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from typing import Optional
from app.core.auth import verify_password
from passlib.context import CryptContext
import hashlib
import base64
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_all_users(db: Session):
    return db.query(User).all()

def get_user(user_id: int, db: Session):
    return db.get(User, user_id)

def update_user(user_id: int, user_update: UserUpdate, db: Session):
    user = db.get(User, user_id)
    if not user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def destroy_user(user_id: int, db:Session):
    user = db.get(User, user_id)
    db.delete(user)
    db.commit()
    return {"message": "user destroyed"}

def get_password_hash(password: str) -> str:
    sha256_digest = hashlib.sha256(password.encode('utf-8')).digest()
    b64_encoded = base64.b64encode(sha256_digest).decode('utf-8')
    return pwd_context.hash(b64_encoded)
    

def create_user(user_create: UserCreate, db: Session):
    hashed_pw = get_password_hash(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        password=hashed_pw
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
# Add these functions to your existing user_service.py

def get_user_by_username(username: str, db: Session) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()  # type: ignore

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """Authenticate user with username and password"""
    user = get_user_by_username(username, db)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user