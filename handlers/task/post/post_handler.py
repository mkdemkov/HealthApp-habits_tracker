from datetime import datetime
import json
from database.database import add_task_to_database

from flask import request


def register_new_task():
    data = request.get_json()  # получим тело запроса
    email = data.get('email')  # получим email и обработаем его
    if email is None:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['email']['email_not_given']
    if not "@" in str(email):
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['email']['email_incorrect_format']

    name = data.get('name')  # получим название задачи и обработаем его
    if name is None:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['name']['name_is_empty']

    desc = str(data.get('desc'))  # получим описание
    if desc is None:
        desc = ""

    deadline = data.get('deadline')
    if deadline is None:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['deadline']['deadline_is_empty']
    try:
        deadline = datetime.fromisoformat(str(deadline))
    # возможный эксепшн, если дедлайн задан в неправильном формате
    except:
        with open('static/json/errors.json') as file:
            errors_data = json.load(file)
            return errors_data['deadline']['deadline_wrong_format']

    priority = data.get('priority')  # получим приоритет задачи
    if priority is None:
        priority = 1
    else:
        priority = int(priority)

    add_task_to_database(email, name, desc, deadline, priority)  # запишем новую задачу в базу данных

    return {
        "code": 200,
        "info": "Задача успешно добавлена!"
    }


def edit_task():
    pass
