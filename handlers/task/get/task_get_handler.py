from flask import request
import json
from database.database import tasks_from_db, remove_task_from_db


# Обработчик удаления задачи
def remove_task():
    id = request.args.get('id')
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)
    if id is None:
        return errors_data['task_id']['id_is_empty']
    try:
        id = int(id)
    except:
        return errors_data['task_id']['id_wrong_format']
    return remove_task_from_db(id)


# Обработчик получения списка всех задач
def get_all_tasks():
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)

    email = str(request.args.get('email'))
    if email is None:
        return errors_data['email']['email_not_given']

    if '@' not in email:
        return errors_data['email']['email_incorrect_format']

    tasks = tasks_from_db(email)
    task_list = {}
    index = 1
    if len(tasks) == 0:
        return {
            'code': 200,
            'info': 'У вас нет задач!'
        }
    for task in tasks:
        task_list[f'Задача {index}'] = {
            'id': task.id,
            'name': task.name,
            'deadline': task.deadline
        }
        index += 1

    return task_list
