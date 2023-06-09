import os
from datetime import datetime
from dotenv import load_dotenv
from entities.tasks import Tasks
from entities.habits import Habits
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session


def setup():
    try:
        load_dotenv()
        engine = create_engine(os.getenv('path_to_database'))
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        return session
    except:
        return None


# Функция для добавления задача в базу данных
def add_task_to_database(email: str, name: str, desc: str, deadline: datetime, priority: int):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    task = Tasks(email=email, name=name, desc=desc, deadline=deadline, priority=priority)  # создаем объект задача
    session.add(task)
    session.commit()
    session.close()


# Функция для обновление задачи по task_id
def update_task(task_id: int, new_name: str, new_desc: str, new_deadline: datetime, new_priority: int):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    row = session.query(Tasks).filter_by(id=task_id).first()  # извлекаем запись из БД

    session.query(Tasks).filter(Tasks.id == task_id).update(
        {'name': new_name, 'desc': new_desc, 'deadline': new_deadline,
         'priority': new_priority})  # обновляем запись в БД
    session.commit()
    session.close()

    return row


# Функция для добавления привычки в базу данных
def add_habit_to_database(email: str, name: str, desc: str, for_time: int):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    habit = Habits(email=email, name=name, desc=desc, for_time=for_time)  # создаем объект привычка
    session.add(habit)
    session.commit()
    session.close()


# Функция обновления привычки
def update_habit(habit_id: int, new_name: str, new_desc: str, new_for_time: int):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    row = session.query(Habits).filter_by(id=habit_id).first()  # извлечение записи из БД

    session.query(Habits).filter(Habits.id == habit_id).update(
        {'name': new_name, 'desc': new_desc, 'for_time': new_for_time})  # обновление записи в БД
    session.commit()
    session.close()

    return row


# Функция получения всех задач из БД
def tasks_from_db(email: str):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    tasks = session.query(Tasks).filter_by(email=email).all()  # получим все задачи из БД
    session.close()
    return tasks


# Функция получения всех привычек из БД
def habits_from_db(email: str):
    session = setup()

    if session is None:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }

    habits = session.query(Habits).filter_by(email=email).all()  # получим все привычки из БД
    session.close()
    return habits


# Функция для удаления привычки из БД
def remove_habit_from_db(id: int):
    try:
        load_dotenv()
        engine = create_engine(os.getenv('path_to_database'))
        with Session(engine) as session:
            record_to_delete = session.query(Habits).filter_by(
                id=id).one_or_none()  # получим запись, которую надо удалить
            if record_to_delete is not None:  # проверка есть ли она вообще и вывод соответсвующего сообщения
                session.delete(record_to_delete)
                session.commit()
                return {
                    "code": 200,
                    "info": "Привычка успешно удалена!"
                }
            else:
                return {
                    "code": 400,
                    "info": "Нет привычки с заданным id"
                }
    except:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }


# Функция для удаления задачи из БД
def remove_task_from_db(id: int):
    try:
        load_dotenv()
        engine = create_engine(os.getenv('path_to_database'))
        with Session(engine) as session:
            record_to_delete = session.query(Tasks).filter_by(id=id).one_or_none()  # получим запись из БД
            if record_to_delete is not None:
                session.delete(record_to_delete)
                session.commit()
                return {
                    "code": 200,
                    "info": "Задача успешно удалена!"
                }
            else:
                return {
                    "code": 400,
                    "info": "Нет задачи с заданным id"
                }
    except:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }


# Функция для импортирования привычек другого пользователя
def import_habits_from_db(email: str, other_email: str):
    try:
        habits_to_import = habits_from_db(other_email)
        if len(habits_to_import) == 0:
            return {
                'code': 200,
                'info': 'У пользователя, привычки которого вы хотите импортировать, они отсутствуют!'
            }
        for habit in habits_to_import:
            add_habit_to_database(email, habit.name, habit.desc, habit.for_time)
        return {
            'code': 200,
            'info': 'Привычки успешно импортированы!'
        }
    except:
        return {
            "code": 500,
            "info": "Что-то пошло не так при подключении к базе данных"
        }
