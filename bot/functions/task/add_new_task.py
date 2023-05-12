from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import session
from bot.ent.user_task import user_task
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Form(StatesGroup):
    habit = State()  # состояние для ожидания ввода привычки


async def new_task(message: types.Message):
    await message.answer("Пожалуйста, введите название привычки.")
    await Form.habit.set()


async def create_task(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))  # замените на вашу строку подключения
    Session = sessionmaker(bind=engine)
    session = Session()
    async with state.proxy() as data:
        data['habit'] = message.text

    new_habit = user_task(
        id=message.from_user.id,
        email="email@example.com",  # замените на реальный email
        name=data['habit'],
        desc="Описание привычки",  # замените на реальное описание
        deadline=2020-11-14,
        priority=1
    )
    session.add(new_habit)
    session.commit()

    await message.answer(f"Привычка '{data['habit']}' была успешно добавлена!")
    await state.finish()
