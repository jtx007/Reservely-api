from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, security
from app.db.dependency import get_db
from app.models.user import User


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure user is active (extend with additional checks if needed)."""
    if not getattr(current_user, "is_active", True):  # optional safety check
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Return current user if authenticated, otherwise None."""
    if not credentials:
        return None
    try:
        return get_current_user(credentials=credentials, db=db)
    except Exception:
        return None
