import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from bot.ent.user import User
from bot.ent.user_habit import UserHabit


class FormHabit(StatesGroup):
    habit = State()  # состояние для ожидания ввода привычки
    description = State()
    for_time = State()


async def new_habit(message: types.Message):
    await message.answer("Пожалуйста, введите название привычки.")
    await FormHabit.habit.set()


async def create_habit(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        await state.reset_state()
        return
    # Когда пользователь вводит количество дней
    days = int(message.text)
    completion_date = datetime.now() + timedelta(days=days)
    async with state.proxy() as data:
        new_habit = UserHabit(
            id=message.from_user.id,
            email=user.email,
            name=data['habit'],
            desc=data['description'],
            for_time=completion_date
        )
        print("s")
        session.add(new_habit)
        session.commit()
    await message.answer(f"Привычка '{data['habit']}' была успешно добавлена!")
    await state.finish()


async def add_desc_habit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['habit'] = message.text
    await message.answer("Введите описание привычки.")
    await FormHabit.description.set()  # Переходим к состоянию описания задачи


async def add_deadline_habit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("Введите количество дней до соблюдения привычки.")
    await FormHabit.for_time.set()
