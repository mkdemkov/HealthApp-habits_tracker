import datetime
import os
from dotenv import load_dotenv
from flask import Flask
from handlers.habit.post.post_handler import register_new_habit, edit_habit
from handlers.habit.get.get_handler import remove_habit, get_all_habits
from handlers.task.post.post_handler import register_new_task, edit_task
from handlers.task.get.get_handler import remove_task, get_all_tasks
from entities.tasks import Tasks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


@app.route('/task/new', methods=['POST'])
def post_task_new():
    return register_new_task()


@app.route('/task/remove', methods=['GET'])
def get_task_remove():
    return remove_task()


@app.route('/task/edit', methods=['POST'])
def post_task_edit():
    return edit_task()


@app.route('/task/list', methods=['GET'])
def get_task_list():
    return get_all_tasks()


@app.route('/habit/new', methods=['POST'])
def post_habit_new():
    return register_new_habit()


@app.route('/habit/remove', methods=['GET'])
def get_habit_remove():
    return remove_habit()


@app.route('/habit/edit', methods=['POST'])
def post_habit_edit():
    return edit_habit()


@app.route('/habit/list', methods=['GET'])
def get_habit_list():
    return get_all_habits()


@app.route('/')
def index():
    return 'Hello, World!'


def test():
    load_dotenv()
    engine = create_engine(os.getenv('path_to_database'))
    Session = sessionmaker(bind=engine)
    session = Session()

    task = Tasks(email='test', name='Misha', desc='Dick', deadline=datetime.datetime(2023, 12, 24), priority=3)
    session.add(task)
    session.commit()
    session.close()


if __name__ == '__main__':
    test()
    # app.run(debug=True)
