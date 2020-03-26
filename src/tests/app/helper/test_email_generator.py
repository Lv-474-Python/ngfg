import pytest
from app.helper.email_generator import generate_share_field_message
from app.models import Field

import mock


@mock.patch('flask.url_for')
def test_generate_share_field_message(url_mock):
    email = 'test@gmail.com'
    field = {
        'id': 1,
        'name': 'TestField',
        'owner_id': 2,
        'field_type': 1,
        'is_strict': False
    }

    url_mock.return_value = 'link'

    print(generate_share_field_message(email, field))
