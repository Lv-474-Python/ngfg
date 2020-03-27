import pytest
import mock

from app.services import FormFieldService
from app.models import FormField


@pytest.fixture()
def form_field_data():
    data = {'form_id': 1, 'field_id': 1, 'question': 'string', 'position': 1}
    return data


@pytest.fixture()
def form_field_id():
    return 1


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


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormField.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id_redis_is_none(redis_manager_get_mock, query_mock, redis_manager_set_mock, form_field_data):
    instance = FormField(**form_field_data)

    redis_manager_get_mock.return_value = None
    query_mock.get.return_value = instance
    redis_manager_set_mock.return_value = None

    test_instance = FormFieldService.get_by_id(1)

    assert instance == test_instance


@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id_redis_is_not_none(redis_manager_get_mock, form_field_data):
    instance = FormField(**form_field_data)

    redis_manager_get_mock.return_value = instance

    test_instance = FormFieldService.get_by_id(1)

    assert instance == test_instance
