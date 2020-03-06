"""
Base router view.
"""
import jwt

from app import APP
from app.celery_tasks.share_field import call_share_field_task
from app.helper.email_generator import SECRET_KEY
from app.services import FieldService


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    call_share_field_task(["just_mail@gmail.com"],
                          FieldService.to_json(FieldService.get_by_id(1), many=False))
    return 'Hello, World!'


@APP.route('/receive_field/<token>')
def receive_field(token):
    """
    example

    :return: str
    """
    field = jwt.decode(token, SECRET_KEY, algorithms='HS256', verify=False)
    return f'Field that you\'ve ({field["recipient"]}) received: {field["field"]}'
