from flask import request


def post_handler():
    data = request.get_json()
    return f"Received data: {data}"
