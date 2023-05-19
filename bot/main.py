import os
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.functions.keyboards import reg_keyboard
from bot.functions.reg.registration import cmd_register, process_email, UserState
from functions.dec.dec import dp
from functions.task.add_new_task import new_task, create_task, Form, add_desc, add_deadline


engine = create_engine(os.getenv("path_to_database"))
Session = sessionmaker(bind=engine)
session = Session()

dp.register_message_handler(process_email, state=UserState.enter_email)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Вас приветствует HealthAppTrackerBot! Введите email для регистрации",
                         reply_markup=reg_keyboard.keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'добавить привычку')
def add_new_task(message: types.Message):

    return new_task(message)


dp.register_message_handler(add_desc, state=Form.task)
dp.register_message_handler(add_deadline, state=Form.description)
dp.register_message_handler(create_task, state=Form.deadline)


dp.register_message_handler(cmd_register, lambda message: message.text.lower() == 'зарегистрироваться')

if __name__ == '__main__':
    executor.start_polling(dp)
