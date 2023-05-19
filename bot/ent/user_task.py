<<<<<<< HEAD
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
=======
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
>>>>>>> cb829555395ef142c8cd404359eb759ed36fee13


class User_task(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    email: str
    name: str
    desc: str
    deadline: datetime
    priority: int
