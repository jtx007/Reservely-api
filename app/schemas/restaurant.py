from pydantic import BaseModel
from typing import Optional

class RestaurantBase(BaseModel):
    name: str
    description: str

class RestaurantCreate(RestaurantBase):
    open: int
    close: int

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    open: Optional[int] = None
    close: Optional[int] = None

class RestaurantRead(RestaurantBase):
    id: int
    open: int
    close: int

    class Config:
        from_attributes = True
