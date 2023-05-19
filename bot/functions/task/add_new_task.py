import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.ent.user import User
from bot.ent.user_task import User_task


class Form(StatesGroup):
    task = State()  # состояние для ожидания ввода привычки
    description = State()


async def new_task(message: types.Message):
    await message.answer("Пожалуйста, введите название привычки.")
    await Form.task.set()


async def create_task(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))
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
        data['description'] = message.text

    new_task = User_task(
        id=message.from_user.id,
        email=user.email,
        name=data['task'],
        desc=data['description'],  # We are using the description entered by the user
        deadline=(2020, 11, 14),
        priority=1
    )
    session.add(new_task)
    session.commit()

    await message.answer(f"Задача '{data['task']}' была успешно добавлена!")
    await state.finish()


async def add_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task'] = message.text  # Here we are saving the description
    await message.answer("Введите описание задачи.")
    await Form.description.set()