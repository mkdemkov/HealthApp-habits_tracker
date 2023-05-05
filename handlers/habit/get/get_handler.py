from flask import request
from database.database import habits_from_db
from entities.habits import Habits


def remove_habit():
    pass


def get_all_habits():
    email = str(request.args.get('email'))
    habits = habits_from_db(email)

    habits_list = []
    for habit in habits:
        habits_list.append({
            'id': habit.id,
            'name': habit.name,
            #  'email': task.email
            'deadline': habit.deadline
        })

    return habits_list