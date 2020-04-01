"""
Email generator module
"""
import jwt
from flask import url_for
from flask_mail import Message

from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM, URL_DOMAIN


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

def generate_share_form_to_group_user_message(
        recipient,
        group_name,
        form_title,
        token):
    """
    Generate message that will be sent to group user

    :param recipient: group user's email
    :param group_name: name of group to which form will be shared
    :param form_title: title of form that will be shared
    :param token: form token
    """
    #TODO - change url domain
    link = 'http://' + URL_DOMAIN + token
    msg = Message(f"Shared form '{form_title}'", recipients=[recipient])
    msg.html = f"""
        <h3>Hello, {recipient}!<h3>
        <p>As a member of '{group_name}' group you can pass '{form_title}' form</p>
        <p>To pass click on <a href="{link}">this link </a></p>
    """
    return msg

def generate_share_form_to_user_message(
        recipient,
        form_title,
        token):
    """
    Generate message that will be sent to user

    :param recipient: group user's email
    :param form_title: title of form that will be shared
    :param token: form token
    """
    #TODO - change url domain (from localhost)
    link = 'http://' + URL_DOMAIN + token
    msg = Message(f"Shared form '{form_title}'", recipients=[recipient])
    msg.html = f"""
        <h3>Hello, {recipient}!<h3>
        <p>Form "{form_title}" was shared with you</p>
        <p>To pass click on <a href="{link}">this link </a></p>
    """
    return msg
