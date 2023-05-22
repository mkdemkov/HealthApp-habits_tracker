import os

from datetime import datetime
from aiogram import executor
from aiogram import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.functions.habit.add_new_habit import new_habit, add_desc_habit, FormHabit, add_deadline_habit, create_habit
from bot.functions.keyboards import reg_keyboard
from bot.functions.reg.registration import cmd_register, process_email, UserState
from bot.functions.task.delete_task import cmd_delete_task, process_task_to_delete, DeleteForm
from bot.functions.habit.delete_habit import cmd_delete_habbit, process_habbit_to_delete ,DeleteHabit
from functions.dec.dec import dp
from functions.task.add_new_task import new_task, create_task, Form, add_desc, add_deadline, add_priority
from bot.ent.user import User
from bot.ent.user_task import UserTask
<<<<<<< HEAD
=======
from bot.ent.user_habit import UserHabit

>>>>>>> 0cd63ccd136ca785c7578b3cd0635875e7a3efd6

engine = create_engine(os.getenv("path_to_database"))
Session = sessionmaker(bind=engine)
session = Session()

dp.register_message_handler(process_email, state=UserState.enter_email)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Вас приветствует HealthAppTrackerBot! Нажмите зарегистрироваться для того чтобы начать работу",
                         reply_markup=reg_keyboard.keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'добавить задачу')
def add_new_task(message: types.Message):
    return new_task(message)


@dp.message_handler(lambda message: message.text.lower() == 'добавить привычку')
def add_new_habit(message: types.Message):
    return new_habit(message)


@dp.message_handler(commands='tasks')
async def cmd_tasks(message: types.Message):
    # Получаем пользователя из базы данных
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    # Получаем все задачи этого пользователя
    tasks = session.query(UserTask).filter_by(id=message.from_user.id).all()
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    # Формируем сообщение со списком задач
    tasks_text = "\n".join(
        f"{task.name}, дедлайн: {task.deadline.strftime('%Y-%m-%d')}, приоритет: {task.priority}"
        for task in tasks
    )

    await message.answer(f"Ваши задачи:\n{tasks_text}")


@dp.message_handler(lambda message: message.text.lower() == 'список задач')
async def button_tasks(message: types.Message):
    # Получаем пользователя из базы данных
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    # Получаем все задачи этого пользователя
    tasks = session.query(UserTask).filter_by(id=message.from_user.id).all()
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    # Формируем сообщение со списком задач
    tasks_text = "\n".join(
        f"{idx + 1}) {task.name}, дедлайн: {task.deadline.strftime('%Y-%m-%d')}, приоритет: {task.priority}"
        for idx, task in enumerate(tasks)
    )

    await message.answer(f"Ваши задачи:\n{tasks_text}")

@dp.message_handler(lambda message: message.text.lower() == 'список привычек')
async def button_habit(message: types.Message):
    # Получаем пользователя из базы данных
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    # Получаем все привычки этого пользователя
    habit = session.query(UserHabit).filter_by(id=message.from_user.id).all()
    if not habit:
        await message.answer("У вас пока нет привычек.")
        return
    # Формируем сообщение со списком привычек
    habit_text = "\n".join(
        f"{idx + 1}) {habit.name}, дней до соблюдения: {'привычка завершена' if (habit.for_time - datetime.now().date()).days <= 0 else (habit.for_time - datetime.now().date()).days}"
        for idx, habit in enumerate(habit)
    )

    await message.answer(f"Ваши привычки:\n{habit_text}")

dp.register_message_handler(add_desc, state=Form.task)
dp.register_message_handler(add_deadline, state=Form.description)
dp.register_message_handler(add_priority, state=Form.deadline)
dp.register_message_handler(create_task, state=Form.priority)
dp.register_message_handler(cmd_delete_task, lambda message: message.text.lower() == 'удалить задачу')
dp.register_message_handler(process_task_to_delete, state=DeleteForm.task_to_delete)

dp.register_message_handler(add_desc_habit, state=FormHabit.habit)
dp.register_message_handler(add_deadline_habit, state=FormHabit.description)
dp.register_message_handler(create_habit, state=FormHabit.for_time)
dp.register_message_handler(cmd_delete_habbit, lambda message: message.text.lower() == 'удалить привычку')
dp.register_message_handler(process_habbit_to_delete, state=DeleteHabit.habit_to_delete)

dp.register_message_handler(cmd_register, lambda message: message.text.lower() == 'зарегистрироваться')

if __name__ == '__main__':
    executor.start_polling(dp)
