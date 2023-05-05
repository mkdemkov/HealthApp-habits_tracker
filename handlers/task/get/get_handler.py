from flask import request
from sqlalchemy import create_engine, Column, Integer, String
from dotenv import load_dotenv
from entities.tasks import Tasks
from sqlalchemy.orm import sessionmaker
from database.database import tasks_from_db
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Session, create_engine
import os


def remove_task():
    id = request.args.get('id')
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    with Session(engine) as session:
        value = 42
        record_to_delete = session.query(Tasks).filter_by(id=id).one_or_none()

        if record_to_delete is not None:
            session.delete(record_to_delete)
            session.commit()
            print(f"Запись с id {value} успешно удалена.")
        else:
            print(f"Запись с id {value} не найдена.")


def get_all_tasks():
    email = str(request.args.get('email'))
    tasks = tasks_from_db(email)
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'name': task.name,
            'deadline': task.deadline
        })

    return task_list
