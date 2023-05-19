from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import session
from bot.ent.user_task import User_task
from bot.ent.user import User

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class Form(StatesGroup):
    task = State()  # состояние для ожидания ввода привычки
    description = State()  # состояние для ожидания ввода описания задачи


async def new_task(message: types.Message):
    await message.answer("Пожалуйста, введите название привычки.")
    await Form.task.set()


async def create_task(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))  # замените на вашу строку подключения
    Session = sessionmaker(bind=engine)
    session = Session()

    # Проверяем, есть ли пользователь с таким id в базе данных
    user = session.query(User).filter_by(id=message.from_user.id).first()

    # Если пользователь не существует или у него нет email, возвращаем сообщение
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        await state.reset_state()  # Сбрасываем состояние
        return

    async with state.proxy() as data:
        data['task'] = message.text

    new_task = User_task(
        id=message.from_user.id,
        email=user.email,
        name=data['task'],
        desc="Описание задачи",  # замените на реальное описание
        deadline=(2020, 11, 14),
        priority=1
    )
    session.add(new_task)
    session.commit()

    await message.answer(f"Задача '{data['habit']}' была успешно добавлена!")
    await state.finish()

