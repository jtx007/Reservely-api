from sqlalchemy.orm import Session
from schemas.user import UserCreate
from models.user import User
from passlib.context import CryptContext
import hashlib
import base64
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_users(db: Session):
    return db.query(User).all()

def get_password_hash(password: str) -> str:
    sha256_digest = hashlib.sha256(password.encode('utf-8')).digest()
    b64_encoded = base64.b64encode(sha256_digest).decode('utf-8')
    return pwd_context.hash(b64_encoded)
    
def create_user(user_create: UserCreate, db: Session):
   print(f"Raw password: {user_create.password}")
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
