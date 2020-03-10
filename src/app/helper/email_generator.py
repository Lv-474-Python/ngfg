"""
Email generator module
"""
import jwt
from flask import url_for
from flask_mail import Message

from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM


def generate_share_field_message(recipient, field):
    """
    Generate message instance

    :param recipient:
    :param field:
    :return: Message instance
    """
    token = jwt.encode(
        {
            'recipient': recipient,
            'field': field['name'],
        },
        SECRET_KEY,
        algorithm=JWT_ALGORITHM)
    link = url_for('receive_field', token=token, _external=True)
    msg = Message('Shared Field', recipients=[recipient])
    msg.html = f'<h3>Hello, {recipient}!\n' +  \
               f'To add field: {field["name"]} to your collection, click this link: {link}</h3>'
    return msg
