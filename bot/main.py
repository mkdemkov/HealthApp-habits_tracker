from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token="6186116061:AAFyCuPyn_d6x1gsvKM87g_w7R7NE-h4psM")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Начало работы бота")

if __name__ == '__main__':
    executor.start_polling(dp)