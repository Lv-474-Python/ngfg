"""
Sockets module
"""
from flask_login import current_user
from flask_socketio import (  # pylint: disable=redefined-builtin
    join_room,
    leave_room,
    ConnectionRefusedError
)


from app import CONNECTIONS_LOGGER, SOCKETIO


@SOCKETIO.on('connect')
def connect():
    """
    Log user that connected via socket (visited front-end)

    """
    if current_user.is_anonymous:
        raise ConnectionRefusedError('Unauthorized')
    join_room(current_user.email)
    CONNECTIONS_LOGGER.info('Connected: %s', current_user.email)


@SOCKETIO.on('disconnect')
def disconnect():
    """
    Log that user disconnected

    """
    leave_room(current_user.email)
    CONNECTIONS_LOGGER.info('Disconnected: %s', current_user.email)
