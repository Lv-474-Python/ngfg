import pytest
from app.helper.email_generator import generate_share_field_message
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


@mock.patch('app.helper.email_generator.url_for')
def test_generate_share_field_message(url_mock, field, app):
    email = 'test@gmail.com'
    link = 'link'

    url_mock.return_value = link

    message = Message('Shared Field', recipients=[email])
    message.html = (
            f'<h3>Hello, {email}!\n' +
            f'To add field: {field["name"]} to your collection, click this link: {link}</h3>'
    )

    result = generate_share_field_message(email, field)

    assert message.html == result.html
