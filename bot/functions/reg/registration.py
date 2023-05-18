import os

from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from bot.functions.dec.dec import dp, storage,token,bot
from bot.ent.user import User


class UserState(StatesGroup):
    enter_email = State()


@dp.message_handler(lambda message: message.text.lower() == "зарегистрироваться")
async def cmd_register(message: types.Message):
    await message.answer("Введите свою почту:")
    await UserState.enter_email.set()


@dp.message_handler(state=UserState.enter_email)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text
    engine = create_engine(os.getenv('path_to_database'))
    Session = sessionmaker(bind=engine)
    session = Session()

    # создание нового пользователя и запись в БД
    new_user = User(email=email)
    session.add(new_user)
    session.commit()

    await state.finish()
    await message.answer("Вы успешно зарегистрировались!")