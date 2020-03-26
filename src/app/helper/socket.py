"""
Sockets module
"""
from flask_login import current_user
from flask_socketio import ConnectionRefusedError  # pylint: disable=redefined-builtin

from app import CONNECTIONS_LOGGER, SOCKETIO


@SOCKETIO.on('connect')
def connect():
    """
    Log user that connected via socket (visited front-end)

    """
    if current_user.is_anonymous:
        raise ConnectionRefusedError('Unauthorized')
    CONNECTIONS_LOGGER.info('Connected: %s', current_user.email)


@SOCKETIO.on('disconnect')
def disconnect():
    """
    Log that user disconnected

    """
    CONNECTIONS_LOGGER.info('Disconnected: %s', current_user.email)


def send_notification(message):
    """
    Send message via socket

    """
    SOCKETIO.send(message)
