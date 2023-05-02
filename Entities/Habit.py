from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# Класс, описывающий таблицу "habits" в базе данных
class Habit(SQLModel, table=True):
    id: Optional[int] = Field(index=True)
    email: str
    name: str
    desc: str
    for_time: int
