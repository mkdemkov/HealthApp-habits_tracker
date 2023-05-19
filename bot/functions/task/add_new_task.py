import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.ent.user_task import User_task


class Form(StatesGroup):
    task = State()  # состояние для ожидания ввода привычки


async def new_task(message: types.Message):
    await message.answer("Пожалуйста, введите название привычки.")
    await Form.task.set()


async def create_task(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))  # замените на вашу строку подключения
    Session = sessionmaker(bind=engine)
    session = Session()
    async with state.proxy() as data:
        data['habit'] = message.text

    new_task = User_task(
        id=message.from_user.id,
        email="email@example.com",  # замените на реальный email
        name=data['habit'],
        desc="Описание задачи",  # замените на реальное описание
        deadline=2020 - 11 - 14,
        priority=1
    )
    session.add(new_task)
    session.commit()

    await message.answer(f"Задача '{data['habit']}' была успешно добавлена!")
    await state.finish()
