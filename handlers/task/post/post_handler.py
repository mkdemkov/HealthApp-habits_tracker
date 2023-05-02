from flask import request


def register_new_task():
    data = request.get_json()
    return f"Received data: {data}"


def edit_task():
    pass