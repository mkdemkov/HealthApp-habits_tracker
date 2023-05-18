import os
from aiogram import executor
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.functions.keyboards import reg_keyboard
from bot.functions.reg.registration import cmd_register
from functions.task.add_new_task import new_task, create_task, Form
from functions.dec.dec import dp, storage,token,bot

engine = create_engine(os.getenv("path_to_database"))  # замените на вашу строку подключения
Session = sessionmaker(bind=engine)
session = Session()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Вас приветствует HealthAppTrackerBot! Введите email для регистрации",
                         reply_markup=reg_keyboard.keyboard)


@dp.message_handler(lambda message: message.text == 'Зарегистрироваться')
async def reg(message: types.Message):
    return cmd_register(message.text)


@dp.message_handler(lambda message: message.text.lower() == 'добавить привычку')
def add_new_task(message: types.Message):
    return new_task(message)  # передайте message в функцию new_task


@dp.message_handler(state=Form.habit)
def process_task(message: types.Message, state: FSMContext):
    return create_task(message, state)


if __name__ == '__main__':
    executor.start_polling(dp)
