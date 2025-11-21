from sqlmodel import Relationship, SQLModel, Field
from typing import Optional

from backend.app.models.room import Room

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    open: int = Field(index=True)
    close: int = Field(index=True)
    description: str
    rooms: list["Room"] = Relationship(back_populates="restaurant")