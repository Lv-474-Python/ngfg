"""
Celery task to send notification
"""

from app import LOGGER, SOCKETIO, CELERY


@CELERY.task(name='ngfg.app.celery_tasks.send_notification.send_notification')
def send_notification(message, current_user_email):
    """
    Send message via socket

    """
    print('SEND NOTIFICATION')
    print(f'{message=}')
    print(f'{current_user_email=}')
    SOCKETIO.send(message, broadcast=False, room=current_user_email)
