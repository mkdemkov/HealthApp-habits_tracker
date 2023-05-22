import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.ent.user import User
from bot.ent.user_habit import UserHabit


class DeleteHabit(StatesGroup):
    habit_to_delete = State()


async def cmd_delete_habbit(message: types.Message):
    engine = create_engine(os.getenv("path_to_database"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    habit = session.query(UserHabit).filter_by(id=message.from_user.id).all()
    if not habit:
        await message.answer("У вас пока нет привычек.")
        return

    habit_text = "\n".join(
        f"{idx + 1}) {habit.name}"
        for idx, habit in enumerate(habit)
    )
    await message.answer(f"Выберите номер привычки для удаления:\n{habit_text}")
    await DeleteHabit.habit_to_delete.set()


async def process_habbit_to_delete(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите числовой номер привычки.")
        return
    engine = create_engine(os.getenv("path_to_database"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    try:
        habit_num = int(message.text) - 1
    except ValueError:
        await message.answer("Неверный номер привычки. Попробуйте еще раз.")
        return
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        await state.reset_state()
        return

    habit = session.query(UserHabit).filter_by(id=message.from_user.id).all()
    if habit_num < 0 or habit_num >= len(habit):
        await message.answer("Неверный номер привычки. Попробуйте еще раз.")
        return

    habit_to_delete = habit[habit_num]
    session.delete(habit_to_delete)
    session.commit()

    await message.answer(f"Привычка '{habit_to_delete.name}' была успешно удалена!")
    await state.finish()
