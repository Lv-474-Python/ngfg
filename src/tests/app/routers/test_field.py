"""
Test Field resource
"""

import mock
import pytest
from flask import jsonify

from app.models import Field, User
from app.services import FieldService

from .routers_test_data import (
    FIELD_RESOURCE_GET_ALL_TRUE_WITH_EXTRA_OPTIONS,
    FIELD_RESOURCE_GET_ALL_TRUE_WITHOUT_EXTRA_OPTIONS,
    FIELD_RESOURCE_GET_ALL_TRUE_WITH_SHARED_FIELDS,
    FIELD_RESOURCE_GET_BY_ID_TRUE_WITH_EXTRA_OPTIONS,
    FIELD_RESOURCE_GET_BY_ID_TRUE_WITHOUT_EXTRA_OPTIONS,
    FIELD_RESOURCE_GET_BY_ID_FORBIDDEN
)


# get all
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
