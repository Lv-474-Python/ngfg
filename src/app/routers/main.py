"""
Base router view.
"""
from app import APP
from app.services import AnswerService


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    AnswerService.test()
    return 'Hello, World!'
