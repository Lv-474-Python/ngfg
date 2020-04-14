"""
Test Field resource
"""

import mock
import pytest
from flask import jsonify

from app.models import Field, User
from app.services import FieldService


# get all
FIELD_RESOURCE_GET_ALL_TRUE_WITH_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'range': {'min': 10, 'max': 100}},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'range': {'min': 100, 'max': 150}},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'choiceOptions': ['1', '2', '3', '4', '5']},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {
            'settingAutocomplete': {
                'dataUrl': 'https://docs.google.com/spreadsheet/d/aua',
                'sheet': 'sheet1',
                'fromRow': 'A1',
                'toRow': 'A13'
            },
            'values': ['1', '2', '3', '4']
        },
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'choiceOptions': ['1', '2', '3', '4'], 'range': {'min': 1, 'max': 2}},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]

@pytest.mark.parametrize(
    "field_json, extra_options, user_json",
    FIELD_RESOURCE_GET_ALL_TRUE_WITH_EXTRA_OPTIONS
)
@mock.patch('app.services.UserService.to_json')
@mock.patch('app.services.UserService.get_by_id')
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.get_shared_fields')
@mock.patch('app.services.FieldService.filter')
def test_get_all_true_with_extra_options(
        mock_field_filter,
        mock_field_get_shared,
        mock_field_get_additional_options,
        mock_user_get,
        mock_user_to_json,
        client,
        login_user,
        field_json,
        extra_options,
        user_json):
    """
    Test FieldsAPI get()
    Test case when fields have extra options
    """
    field = Field(**field_json)
    user = User(**user_json)
    field_json = FieldService.field_to_json(field)

    field_json['owner'] = user_json
    if field_json['ownerId'] == login_user.id:
        field_json['owner']['current'] = True

    for key, value in extra_options.items():
        field_json[key] = value

    mock_field_filter.return_value = [field]
    mock_field_get_shared.return_value = []
    mock_field_get_additional_options.return_value = extra_options
    mock_user_get.return_value = user
    mock_user_to_json.return_value = user_json

    response = client.get(f'api/v1/fields/', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify({"fields": [field_json]}).data


FIELD_RESOURCE_GET_ALL_TRUE_WITHOUT_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]

@pytest.mark.parametrize(
    "field_json, user_json",
    FIELD_RESOURCE_GET_ALL_TRUE_WITHOUT_EXTRA_OPTIONS
)
@mock.patch('app.services.UserService.to_json')
@mock.patch('app.services.UserService.get_by_id')
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.get_shared_fields')
@mock.patch('app.services.FieldService.filter')
def test_get_all_true_without_extra_options(
        mock_field_filter,
        mock_field_get_shared,
        mock_field_get_additional_options,
        mock_user_get,
        mock_user_to_json,
        client,
        login_user,
        field_json,
        user_json):
    """
    Test FieldsAPI get()
    Test case when fields don't have extra options
    """
    field = Field(**field_json)
    user = User(**user_json)
    field_json = FieldService.field_to_json(field)

    field_json['owner'] = user_json
    if field_json['ownerId'] == login_user.id:
        field_json['owner']['current'] = True

    mock_field_filter.return_value = [field]
    mock_field_get_shared.return_value = []
    mock_field_get_additional_options.return_value = {}
    mock_user_get.return_value = user
    mock_user_to_json.return_value = user_json

    response = client.get(f'api/v1/fields/', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify({"fields": [field_json]}).data


FIELD_RESOURCE_GET_ALL_TRUE_WITH_SHARED_FIELDS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'id': 2, 'username': 'name 1', 'email': 'ma@gmail.com', 'google_token': 'aq'}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 2, 'field_type': 2, 'is_strict': True},
        {'id': 3, 'username': 'name 3', 'email': 'm2@gmail.com', 'google_token': 'wq'}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 3, 'field_type': 3},
        {'id': 4, 'username': 'name 4', 'email': 'm4@gmail.com', 'google_token': 'af'}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 4, 'field_type': 4},
        {'id': 5, 'username': 'name 5', 'email': 'mp@gmail.com', 'google_token': 'rq'}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 5, 'field_type': 5},
        {'id': 6, 'username': 'name 6', 'email': 'md@gmail.com', 'google_token': 'ew'}
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 6, 'field_type': 6},
        {'id': 7, 'username': 'name 9', 'email': 'ms@gmail.com', 'google_token': 'al'}
    )
]
@pytest.mark.parametrize(
    "field_json, user_json",
    FIELD_RESOURCE_GET_ALL_TRUE_WITH_SHARED_FIELDS
)
@mock.patch('app.services.UserService.to_json')
@mock.patch('app.services.UserService.get_by_id')
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.get_shared_fields')
@mock.patch('app.services.FieldService.filter')
def test_get_all_true_with_shared_fields(
        mock_field_filter,
        mock_field_get_shared,
        mock_field_get_additional_options,
        mock_user_get,
        mock_user_to_json,
        client,
        login_user,
        field_json,
        user_json):
    """
    Test FieldsAPI get()
    Test case when shared fields are provided
    """
    field = Field(**field_json)
    user = User(**user_json)
    field_json = FieldService.field_to_json(field)

    field_json['owner'] = user_json
    if field_json['ownerId'] == login_user.id:
        field_json['owner']['current'] = True

    mock_field_filter.return_value = []
    mock_field_get_shared.return_value = [field]
    mock_field_get_additional_options.return_value = {}
    mock_user_get.return_value = user
    mock_user_to_json.return_value = user_json

    response = client.get(f'api/v1/fields/', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify({"fields": [field_json]}).data


@mock.patch('app.services.FieldService.get_shared_fields')
@mock.patch('app.services.FieldService.filter')
def test_get_all_true_empty(mock_field_filter, mock_field_get_shared, client):
    """
    Test FieldsAPI get()
    Test case when fields list is empty
    """
    mock_field_filter.return_value = []
    mock_field_get_shared.return_value = []

    response = client.get(f'api/v1/fields/', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify({"fields": []}).data


# get(field_id)
FIELD_RESOURCE_GET_BY_ID_TRUE_WITH_EXTRA_OPTIONS = [
    (
        {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
        {'range': {'min': 10, 'max': 100}}
    ),
    (
        {'id': 2, 'name': 'name 2', 'owner_id': 1, 'field_type': 2, 'is_strict': True},
        {'range': {'min': 100, 'max': 150}}
    ),
    (
        {'id': 3, 'name': 'name 3', 'owner_id': 1, 'field_type': 3},
        {}
    ),
    (
        {'id': 4, 'name': 'name 4', 'owner_id': 1, 'field_type': 4},
        {'choiceOptions': ['1', '2', '3', '4', '5']}
    ),
    (
        {'id': 5, 'name': 'name 5', 'owner_id': 1, 'field_type': 5},
        {
            'settingAutocomplete': {
                'dataUrl': 'https://docs.google.com/spreadsheet/d/aua',
                'sheet': 'sheet1',
                'fromRow': 'A1',
                'toRow': 'A13'
            },
            'values': ['1', '2', '3', '4']
        }
    ),
    (
        {'id': 6, 'name': 'name 6', 'owner_id': 1, 'field_type': 6},
        {'choiceOptions': ['1', '2', '3', '4'], 'range': {'min': 1, 'max': 2}}
    )
]

@pytest.mark.parametrize(
    "field_json, extra_options",
    FIELD_RESOURCE_GET_BY_ID_TRUE_WITH_EXTRA_OPTIONS
)
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.field_to_json')
@mock.patch('app.services.FieldService.get_by_id')
def test_get_by_id_true_with_extra_options(
        mock_field_get,
        mock_field_to_json,
        mock_field_get_additional_options,
        client,
        field_json,
        extra_options):
    """
    Test FieldAPI get()
    Test case when field has extra options
    """
    field = Field(**field_json)
    mock_field_get.return_value = field
    mock_field_to_json.return_value = field_json
    mock_field_get_additional_options.return_value = extra_options

    for key, value in extra_options.items():
        field_json[key] = value

    response = client.get(f'api/v1/fields/{field.id}', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify(field_json).data


FIELD_RESOURCE_GET_BY_ID_TRUE_WITHOUT_EXTRA_OPTIONS = [
    {'id': 1, 'name': 'name 1', 'owner_id': 1, 'field_type': 1, 'is_strict': True},
    {'id': 2, 'name': 'name 2', 'owner_id': 1, 'field_type': 2, 'is_strict': True},
    {'id': 3, 'name': 'name 3', 'owner_id': 1, 'field_type': 3},
    {'id': 4, 'name': 'name 4', 'owner_id': 1, 'field_type': 4},
    {'id': 5, 'name': 'name 5', 'owner_id': 1, 'field_type': 5},
    {'id': 6, 'name': 'name 6', 'owner_id': 1, 'field_type': 6}
]

@pytest.mark.parametrize(
    "field_json",
    FIELD_RESOURCE_GET_BY_ID_TRUE_WITHOUT_EXTRA_OPTIONS
)
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.field_to_json')
@mock.patch('app.services.FieldService.get_by_id')
def test_get_by_id_true_without_extra_options(
        mock_field_get,
        mock_field_to_json,
        mock_field_get_additional_options,
        client,
        field_json):
    """
    Test FieldAPI get()
    Test case when field doesn't have extra options
    """
    field = Field(**field_json)
    mock_field_get.return_value = field
    mock_field_to_json.return_value = field_json
    mock_field_get_additional_options.return_value = {}

    response = client.get(f'api/v1/fields/{field.id}', follow_redirects=True)

    assert response.status_code == 200
    assert response.data == jsonify(field_json).data


@mock.patch('app.services.FieldService.get_by_id')
def test_get_by_id_field_not_exist(mock_field_get, client):
    """
    Test FieldAPI get()
    Test case when field doesn't exist
    """
    mock_field_get.return_value = None

    field_id = 1
    response = client.get(f'api/v1/fields/{field_id}', follow_redirects=True)

    assert response.status_code == 400
    assert response.json['message'] == "Field does not exist"


FIELD_RESOURCE_GET_BY_ID_FORBIDDEN = [
    ({'id': 2, 'name': 'name 1', 'owner_id': 2, 'field_type': 1}),
    ({'id': 3, 'name': 'name 1', 'owner_id': 3, 'field_type': 1}),
    ({'id': 4, 'name': 'name 1', 'owner_id': 4, 'field_type': 1}),
]
@pytest.mark.parametrize(
    "field_json",
    FIELD_RESOURCE_GET_BY_ID_FORBIDDEN
)
@mock.patch('app.services.FieldService.get_by_id')
def test_get_by_id_forbidden(mock_field_get, field_json, client):
    """
    Test FieldAPI get()
    Test case when user cannot get field because he isn't owner
    """
    field = Field(**field_json)
    mock_field_get.return_value = field

    response = client.get(f'api/v1/fields/{field.id}', follow_redirects=True)

    assert response.status_code == 403
    assert response.json['message'] == "Forbidden. User is not the field owner"
