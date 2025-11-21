from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from backend.app.models.restaurant import Restaurant

class Room(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str = Field(default=None)
  description: str
  restaurant_id: int = Field(nullable=False, default=None, foreign_key="restaurant.id")
  restaurant: Restaurant = Relationship(back_populates="rooms")