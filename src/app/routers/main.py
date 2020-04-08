"""
Base router view.
"""
import jwt

from app import APP, SOCKETIO
from app.celery_tasks.share_field import call_share_field_task
from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM
from app.services import FieldService
from app.celery_tasks.send_notification import send_notification


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    SOCKETIO.send('yura1', broadcast=False)
    SOCKETIO.send('yura2', broadcast=True)
    SOCKETIO.emit('message', {'notification': 'DAROVA1'}, broadcast=False)
    SOCKETIO.emit('message', {'notification': 'DAROVA2'}, broadcast=True)
    SOCKETIO.emit('message2312', broadcast=True, room='2')
    # SOCKETIO.emit('message', {'notification': 'DAROVA'}, broadcast=False)

    send_notification.apply_async(args=['DAAAA', 'yurdosii.ksv@gmail.com'])


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
    call_share_field_task(['justMail@gmail.com'],
                          FieldService.field_to_json(FieldService.get_by_id(21), many=False))
    return 'Message sent!'
