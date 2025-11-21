from pydantic import BaseModel
from typing import Optional

from backend.app.models import restaurant
from backend.app.models.restaurant import Restaurant

class RoomBase(BaseModel):
  name: str
  description: str
  
class RoomCreate(RoomBase):
  restaurant_id: int

class RoomUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None


class RoomRead(RoomBase):
  id: int
  restaurant: Restaurant