"""
Base router view.
"""
from app import APP

@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    return 'Hello, World!'
