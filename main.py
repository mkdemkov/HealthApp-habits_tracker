from flask import Flask
from handlers.habit.post.post_handler import post_handler

app = Flask(__name__)


@app.route('/habit/list', methods=['POST'])
def post():
    return post_handler()


@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
