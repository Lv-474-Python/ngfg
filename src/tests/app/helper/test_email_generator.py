import pytest
from app.helper.email_generator import generate_share_field_message
from app.helper.constants import URL_DOMAIN
from flask_mail import Message

import mock


@pytest.fixture
def field():
    data = {
        'id': 1,
        'name': 'TestField',
        'owner_id': 2,
        'field_type': 1,
        'is_strict': False
    }

    return data


def test_generate_share_field_message( field, app):
    email = 'test@gmail.com'
    link = 'http://' + URL_DOMAIN + '/fields'

    message = Message('Shared Field', recipients=[email])
    message.html = (f"""
        <h3>Hello, {email}!<h3>
        <p> Field '{field["name"]}' was added to your collection</p>
        <p>To go to your collection click on <a href="{link}">this link</a></p>
    """
    )

    result = generate_share_field_message(email, field)

    assert message.html == result.html
