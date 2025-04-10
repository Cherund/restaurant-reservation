from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="table.id")
    reservation_time: datetime
    duration_minutes: int
