import json
from database.database import add_habit_to_database, update_habit
from flask import request


# Функция для добавления новой привычки
def register_new_habit():
    data = request.get_json()  # получим тело запроса
    email = data.get('email')  # получим email и обработаем его
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)

    if email is None:
        return errors_data['email']['email_not_given']
    if not "@" in str(email):
        return errors_data['email']['email_incorrect_format']

    name = data.get('name')  # получим название привычки и обработаем его
    if name is None:
        return errors_data['name']['name_is_empty']

    desc = str(data.get('desc'))  # получим описание
    if desc is None:
        desc = ""

    for_time = data.get('for_time')
    if for_time is None:
        return errors_data['for_time']['time_not_given']
    try:
        for_time = int(for_time)
    except:
        return errors_data['for_time']['time_wrong_format']

    add_habit_to_database(email, name, desc, for_time)

    return {
        "code": 200,
        "info": "Привычка успешно добавлена!"
    }


# Функция для редактирования привычки
def edit_habit():
    data = request.get_json()  # получим тело запроса
    habit_id = data.get('id')
    with open('static/json/errors.json') as file:
        errors_data = json.load(file)

    if habit_id is None:
        return errors_data['habit_id']['id_is_empty']
    try:
        habit_id = int(habit_id)
    except:
        return errors_data['habit_id']['id_wrong_format']

    new_name = data.get('name')  # получим название задачи и обработаем его
    if new_name is None:
        return errors_data['name']['name_is_empty']

    new_desc = str(data.get('desc'))  # получим описание
    if new_desc is None:
        new_desc = ""

    new_for_time = data.get('for_time')
    if new_for_time is None:
        return errors_data['for_time']['time_not_given']
    try:
        new_for_time = int(new_for_time)
    # возможный эксепшн, если дедлайн привычки в неправильном формате
    except:
        return errors_data['for_time']['time_wrong_format']

    res = update_habit(habit_id, new_name, new_desc, new_for_time)

    if res:
        return {
            "code": 200,
            "info": "Привычка успешно обновлена!"
        }
    return {
        "code": 400,
        "info": "Привычка с таким id не найдена"
    }
