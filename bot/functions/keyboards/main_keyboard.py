from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    types.KeyboardButton("Добавить задачу"),
    types.KeyboardButton("Список задач"),
    types.KeyboardButton("Удалить задачу"),
    types.KeyboardButton("Добавить привычку")
]
keyboard.add(*buttons)
