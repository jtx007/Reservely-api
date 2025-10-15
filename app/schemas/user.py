from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str  # Plain password from client

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
