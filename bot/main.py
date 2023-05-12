from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functions.task.add_new_task import new_task, create_task, Form
from functions.task.add_new_task import new_task, create_task, Form
from dotenv import load_dotenv
import os

bot = Bot(token="6019968937:AAFhXzdcIIcI2AaIVcqrP4h5m2XEciv86mM")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
load_dotenv()
engine = create_engine(os.getenv("path_to_database"))  # замените на вашу строку подключения
Session = sessionmaker(bind=engine)
session = Session()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton("Добавить привычку")]
    keyboard.add(*buttons)
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == 'добавить привычку')
def add_new_task(message: types.Message):
    return new_task(message)  # передайте message в функцию new_task


@dp.message_handler(state=Form.habit)
def process_task(message: types.Message, state: FSMContext):
    return create_task(message, state)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)
