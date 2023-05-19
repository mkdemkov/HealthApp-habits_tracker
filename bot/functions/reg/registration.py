import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.ent.user import User
from bot.functions.dec.dec import dp
from bot.functions.keyboards import add_task_keyboard


class UserState(StatesGroup):
    enter_email = State()


@dp.message_handler(lambda message: message.text.lower() == 'зарегистрироваться')
async def cmd_register(message: types.Message):
    await message.answer("Введите свою почту:")
    await UserState.enter_email.set()  # переходим в состояние ввода email


@dp.message_handler(state=UserState.enter_email)
async def process_email(message: types.Message, state: FSMContext):
    engine = create_engine(os.getenv("path_to_database"))
    Session = sessionmaker(bind=engine)
    session = Session()
    email = message.text  # получаем email от пользователя

    # проверяем, есть ли уже такой пользователь в базе
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        await message.answer("Вы уже зарегистрированы!")
    elif '@' not in message.text:
        await message.answer("Неверный адрес")
    else:
        # сохраняем email в базу данных
        new_user = User(
            email=email,
            id=message.from_user.id
        )
        session.add(new_user)
        session.commit()

        await state.finish()  # заканчиваем работу FSM
        await message.answer("Вы успешно зарегистрировались!", reply_markup=add_task_keyboard.keyboard)
