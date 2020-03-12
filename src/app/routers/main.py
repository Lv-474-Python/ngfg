"""
Base router view.
"""
import jwt

from app import APP
from app.celery_tasks.share_field import call_share_field_task
from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM
from app.services import FieldService


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """

    return 'Hello, World!'


@APP.route('/receive_field/<token>')
def receive_field(token):
    """
    example

    :return: str
    """
    field = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
    return f'Field that you\'ve ({field["recipient"]}) received: {field["field"]}'


@APP.route('/share_message')
def share_message():
    """
    example

    :return: str
    """
    call_share_field_task(["just_mail@gmail.com"],
                          FieldService.field_to_json(FieldService.get_by_id(1), many=False))
    return 'Message sent!'
