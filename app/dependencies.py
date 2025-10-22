from fastapi import Depends
from sqlalchemy.orm import Session
from core.auth import get_current_user
from models.user import User
from db.dependency import get_db

# Re-export the get_current_user dependency for easy access
def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get the current active user (can add additional checks here if needed)"""
    return current_user

# Optional: Create a dependency for optional authentication
def get_current_user_optional(
    db: Session = Depends(get_db)
) -> User | None:
    """Get current user if authenticated, otherwise return None"""
    try:
        return get_current_user(db=db)
    except:
        return None
