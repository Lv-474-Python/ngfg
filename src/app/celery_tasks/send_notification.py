"""
Celery task to send notification
"""

from app import SOCKETIO, CELERY


@CELERY.task(name='ngfg.app.celery_tasks.send_notification.send_notification')
def send_notification(message, current_user_email):
    """
    Send message via socket

    :param message: message to send via socket
    :param current_user_email: socket room
    """
    SOCKETIO.send(message, broadcast=False, room=current_user_email)
