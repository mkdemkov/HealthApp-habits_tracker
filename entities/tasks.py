from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# Класс, описывающий таблицу "tasks" в базе данных
class Tasks(SQLModel, table=True):
    id: Optional[int] = Field(index=True, primary_key=True)
    email: str
    name: str
    desc: str
    deadline: datetime
    priority: int
