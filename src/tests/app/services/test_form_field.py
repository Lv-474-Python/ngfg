import pytest
import mock

from app.services import FormFieldService
from app.models import FormField


@pytest.fixture()
def form_field_data():
    data = {'form_id': 1, 'field_id': 1, 'question': 'string', 'position': 1}
    return data


@pytest.fixture()
def form_field_updated_data():
    data = {'form_id': 2, 'field_id': 2, 'question': 'new_string', 'position': 2}
    return data


@mock.patch('app.DB.session.add')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_create(redis_manager_get_mock, db_mock, form_field_data):
    db_mock.return_value = None
    redis_manager_get_mock.return_value = [FormField(**form_field_data), FormField(**form_field_data)]

    instance = FormField(**form_field_data)
    test_instance = FormFieldService.create(**form_field_data)

    assert instance.form_id == test_instance.form_id
    assert instance.field_id == test_instance.field_id
    assert instance.question == test_instance.question
    assert instance.position == test_instance.position


@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id(redis_manager_get_mock, query_mock, form_field_data):
    instance = FormField(**form_field_data)

    redis_manager_get_mock.return_value = None
    query_mock.get.return_value = instance

    test_instance = FormFieldService.get_by_id(1)

    assert instance == test_instance


@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.merge')
@mock.patch('app.services.FormFieldService.get_by_id')
def test_update(get_by_id_mock, db_mock, redis_manager_get_mock, form_field_data, form_field_updated_data):
    instance = FormField(**form_field_data)

    get_by_id_mock.return_value = instance
    db_mock.return_value = None
    redis_manager_get_mock.return_value = True

    updated_instance = FormField(**form_field_updated_data)

    test_instance = FormFieldService.update(1, **form_field_updated_data)

    assert updated_instance.form_id == test_instance.form_id
    assert updated_instance.field_id == test_instance.field_id
    assert updated_instance.question == test_instance.question
    assert updated_instance.position == test_instance.position


@mock.patch('app.services.FormFieldService.get_by_id')
def test_update_with_form_field_not_exist(get_by_id_mock, form_field_data):
    get_by_id_mock.return_value = None

    test_instance = FormFieldService.update(form_field_data.get('id'))

    assert test_instance == None
