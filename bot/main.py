import os

from aiogram import executor
from aiogram import types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.functions.keyboards import reg_keyboard
from bot.functions.reg.registration import cmd_register, process_email, UserState
from bot.functions.task.delete_task import cmd_delete_task, process_task_to_delete, DeleteForm
from functions.dec.dec import dp
from functions.task.add_new_task import new_task, create_task, Form, add_desc, add_deadline, add_priority
from bot.ent.user import User
from bot.ent.user_task import User_task

engine = create_engine(os.getenv("path_to_database"))
Session = sessionmaker(bind=engine)
session = Session()

dp.register_message_handler(process_email, state=UserState.enter_email)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Вас приветствует HealthAppTrackerBot! Введите email для регистрации",
                         reply_markup=reg_keyboard.keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'добавить задачу')
def add_new_task(message: types.Message):
    return new_task(message)


@dp.message_handler(commands='tasks')
async def cmd_tasks(message: types.Message):
    # Получаем пользователя из базы данных
    user = session.query(User).filter_by(id=message.from_user.id).first()
    if user is None or user.email is None:
        await message.answer("Пожалуйста, сначала зарегистрируйте свою электронную почту.")
        return

    # Получаем все задачи этого пользователя
    tasks = session.query(User_task).filter_by(id=message.from_user.id).all()
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
    tasks = session.query(User_task).filter_by(id=message.from_user.id).all()
    if not tasks:
        await message.answer("У вас пока нет задач.")
        return

    # Формируем сообщение со списком задач
    tasks_text = "\n".join(
        f"{idx+1}) {task.name}, дедлайн: {task.deadline.strftime('%Y-%m-%d')}, приоритет: {task.priority}"
        for idx, task in enumerate(tasks)
    )

    await message.answer(f"Ваши задачи:\n{tasks_text}")


dp.register_message_handler(add_desc, state=Form.task)
dp.register_message_handler(add_deadline, state=Form.description)
dp.register_message_handler(add_priority, state=Form.deadline)
dp.register_message_handler(create_task, state=Form.priority)
dp.register_message_handler(cmd_delete_task, lambda message: message.text.lower() == 'удалить задачу')
dp.register_message_handler(process_task_to_delete, state=DeleteForm.task_to_delete)

dp.register_message_handler(cmd_register, lambda message: message.text.lower() == 'зарегистрироваться')

if __name__ == '__main__':
    executor.start_polling(dp)