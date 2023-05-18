from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [types.KeyboardButton("Зарегистрироваться")]
keyboard.add(*buttons)