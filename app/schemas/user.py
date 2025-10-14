from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    reservations: list

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True