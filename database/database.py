import os
from datetime import datetime
from dotenv import load_dotenv
from entities.tasks import Tasks
from entities.habits import Habits
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session


# Функция для добавления задача в базу данных
def add_task_to_database(email: str, name: str, desc: str, deadline: datetime, priority: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    task = Tasks(email=email, name=name, desc=desc, deadline=deadline, priority=priority)
    session.add(task)
    session.commit()
    session.close()


# Функция для обновление задачи по task_id
def update_task(task_id: int, new_name: str, new_desc: str, new_deadline: datetime, new_priority: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    row = session.query(Tasks).filter_by(id=task_id).first()

    session.query(Tasks).filter(Tasks.id == task_id).update(
        {'name': new_name, 'desc': new_desc, 'deadline': new_deadline, 'priority': new_priority})
    session.commit()
    session.close()

    return row


# Функция для добавления привычки в базу данных
def add_habit_to_database(email: str, name: str, desc: str, for_time: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    habit = Habits(email=email, name=name, desc=desc, for_time=for_time)
    session.add(habit)
    session.commit()
    session.close()


# Функция обновления привычки
def update_habit(habit_id: int, new_name: str, new_desc: str, new_for_time: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    row = session.query(Habits).filter_by(id=habit_id).first()

    session.query(Habits).filter(Habits.id == habit_id).update(
        {'name': new_name, 'desc': new_desc, 'for_time': new_for_time})
    session.commit()
    session.close()

    return row


def tasks_from_db(email: str):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    Ssesion = sessionmaker(bind=engine)
    session = Ssesion()
    tasks = session.query(Tasks).filter_by(email=email).all()
    session.close()
    return tasks


def remove_task_from_db(id: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    with Session(engine) as session:
        record_to_delete = session.query(Tasks).filter_by(id=id).one_or_none()
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
