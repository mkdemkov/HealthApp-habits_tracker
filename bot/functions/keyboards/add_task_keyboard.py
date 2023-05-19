from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton("Добавить задачу"),
    types.KeyboardButton("Список задач")
]
keyboard.add(*buttons)