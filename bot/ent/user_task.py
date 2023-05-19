from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User_task(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str
    name: str
    desc: str
    deadline: datetime
    priority: int
