from flask import Flask
from handlers.habit.post.habit_post_handler import register_new_habit, edit_habit
from handlers.habit.get.habit_get_handler import remove_habit, get_all_habits, import_habits
from handlers.task.post.task_post_handler import register_new_task, edit_task
from handlers.task.get.task_get_handler import remove_task, get_all_tasks

app = Flask(__name__)


# Хэндлер POST запросов на /task/new
@app.route('/task/new', methods=['POST'])
def post_task_new():
    return register_new_task()


# Хэндлер GET запросов на /task/remove
@app.route('/task/remove', methods=['GET'])
def get_task_remove():
    return remove_task()


# Хэндлер POST запросов на /task/edit
@app.route('/task/edit', methods=['POST'])
def post_task_edit():
    return edit_task()


# Хэндлер GET запросов на /task/list
@app.route('/task/list', methods=['GET'])
def get_task_list():
    return get_all_tasks()


# Хэндлер POST запросов на /habit/new
@app.route('/habit/new', methods=['POST'])
def post_habit_new():
    return register_new_habit()


# Хэндлер GET запросов на /habit/remove
@app.route('/habit/remove', methods=['GET'])
def get_habit_remove():
    return remove_habit()


# Хэндлер POST запросов на /habit/edit
@app.route('/habit/edit', methods=['POST'])
def post_habit_edit():
    return edit_habit()


# Хэндлер GET запросов на /habit/list
@app.route('/habit/list', methods=['GET'])
def get_habit_list():
    return get_all_habits()


# Хэндлер GET запросов на /habit/import
@app.route('/habit/import', methods=['GET'])
def get_habit_import():
    return import_habits()


if __name__ == '__main__':
    app.run(debug=True)
