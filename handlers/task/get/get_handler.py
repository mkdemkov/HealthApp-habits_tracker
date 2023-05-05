from flask import request
from sqlalchemy import create_engine, Column, Integer, String
from dotenv import load_dotenv
from entities.tasks import Tasks
import json
from database.database import tasks_from_db, remove_task_from_db
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Session, create_engine
import os


def remove_task():
    id = request.args.get('id')
    if id is None:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['task_id']['id_is_empty']
    try:
        id = int(id)
    except:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['task_id']['id_wrong_format']
    return remove_task_from_db(id)


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
