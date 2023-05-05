import os
from datetime import datetime
from dotenv import load_dotenv
from entities.tasks import Tasks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


# Функция для обноваление задачи по task_id
def update_task(task_id: int, new_name: str, new_desc: str, new_deadline: datetime, new_priority: int):
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    session.query(Tasks).filter(Tasks.id == task_id).update(
        {'name': new_name, 'desc': new_desc, 'deadline': new_deadline, 'priority': new_priority})
    session.commit()
    session.close()
