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
    deadline = State()


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
        new_task = User_task(
            id=message.from_user.id,
            email=user.email,
            name=data['task'],
            desc=data['description'],
            deadline=data['deadline'],  # use the deadline entered by the user
            priority=1
        )
    session.add(new_task)
    session.commit()

    await message.answer(f"Задача '{data['task']}' была успешно добавлена!")
    await state.finish()


async def add_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text  # Save the description
    await message.answer("Введите дедлайн задачи в формате: год месяц день (например, '2023 5 18').")
    await Form.deadline.set()  # Go to the deadline state


async def add_deadline(message: types.Message, state: FSMContext):
    # parse the deadline entered by the user
    try:
        deadline = tuple(map(int, message.text.split()))  # Assuming the input is like "2022 5 18"
    except ValueError:
        await message.answer("Введите дедлайн в правильном формате: год месяц день (например, '2022 5 18').")
        return

    # Save deadline in the state
    await state.update_data(deadline=deadline)

    await message.answer("Дедлайн установлен.")
    await Form.deadline.set()  # Go to the next state


async def add_task_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task'] = message.text  # Save the task name
    await message.answer("Введите описание задачи.")
    await Form.description.set()  # Go to the description state
