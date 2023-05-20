import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.ent.user import User
from bot.ent.user_task import UserTask


class DeleteForm(StatesGroup):
    task_to_delete = State()


async def cmd_delete_task(message: types.Message):
    engine = create_engine(os.getenv("path_to_database"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    tasks = session.query(UserTask).filter_by(id=message.from_user.id).all()
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    tasks_text = "\n".join(
        f"{idx + 1}) {task.name}, дедлайн: {task.deadline.strftime('%Y-%m-%d')}, приоритет: {task.priority}"
        for idx, task in enumerate(tasks)
    )
    await message.answer(f"Выберите номер задачи для удаления:\n{tasks_text}")
    await DeleteForm.task_to_delete.set()


async def process_task_to_delete(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите числовой номер задачи.")
        return
    engine = create_engine(os.getenv("path_to_database"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    try:
        task_num = int(message.text) - 1
    except ValueError:
        await message.answer("Неверный номер задачи. Попробуйте еще раз.")
        return
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        await state.reset_state()
        return

    tasks = session.query(UserTask).filter_by(id=message.from_user.id).all()
    if task_num < 0 or task_num >= len(tasks):
        await message.answer("Неверный номер задачи. Попробуйте еще раз.")
        return

    task_to_delete = tasks[task_num]
    session.delete(task_to_delete)
    session.commit()

    await message.answer(f"Задача '{task_to_delete.name}' была успешно удалена!")
    await state.finish()
