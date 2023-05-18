from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
import os
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
token = os.getenv('token')
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)