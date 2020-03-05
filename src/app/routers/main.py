"""
Base router view.
"""
from app import APP
from app.helper.email_sender import EmailSender


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    EmailSender.send_email(['dziga2000@gmail.com'])
    return 'Hello, World!'
