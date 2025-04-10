from sqlmodel import SQLModel, Field
from typing import Optional


class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    seats: int
    location: str
