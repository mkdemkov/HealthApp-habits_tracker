from flask import request
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from entities.tasks import Tasks
from sqlalchemy.orm import sessionmaker
import os


def remove_task():
    id = request.args.get('id')
    ####


def get_all_tasks():
    email = str(request.args.get('email'))
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    Ssesion = sessionmaker(bind=engine)
    session = Ssesion()
    tasks = session.query(Tasks).filter_by(email=email).all()

    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'name': task.name,
            #  'email': task.email
            'deadline': task.deadline
        })

    return task_list
