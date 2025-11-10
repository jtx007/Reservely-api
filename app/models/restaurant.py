from sqlmodel import SQLModel, Field
from typing import Optional

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    open: int = Field(index=True)
    close: int = Field(index=True)
    description: str