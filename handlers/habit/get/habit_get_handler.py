import json
from flask import request
from database.database import import_habits_from_db, remove_habit_from_db, habits_from_db


# Обработчик удаления привычки
def remove_habit():
    id = request.args.get('id')
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)
    if id is None:
        return errors_data['habit_id']['id_is_empty']
    try:
        id = int(id)
    except:
        return errors_data['habit_id']['id_wrong_format']
    return remove_habit_from_db(id)


# Обработчик получения списка всех привычек
def get_all_habits():
    email = str(request.args.get('email'))
    habits = habits_from_db(email)
    habit_list = {}
    index = 1
    if len(habits) == 0:
        return 'У вас нет привычек!'
    for habit in habits:
        habit_list[f'Привычка {index}'] = {
            'id': habit.id,
            'name': habit.name,
            'for_time': habit.for_time
        }
        index += 1

    return habit_list


# Обработчик импортирования привычек другого пользователя
def import_habits():
    email = request.args.get('email')
    other_email = request.args.get('other_email')
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)
    if email is None or other_email is None:
        return errors_data['email']['one_of_emails_not_given']
    if not '@' in str(email) or not '@' in str(other_email):
        return errors_data['email']['one_of_emails_incorrect_format']

    return import_habits_from_db(email, other_email)
