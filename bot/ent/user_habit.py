from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class UserHabit(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str
    name: str
    desc: str
    count: Optional[int] = Field(primary_key=True, index=True)
    for_time: int
