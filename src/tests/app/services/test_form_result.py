import pytest
import mock

from app.services import FormResultService
from app.models import FormResult


@pytest.fixture()
def answer_data():
    data = {
        'user_id': 1,
        'form_id': 1,
        'answers': {
            'name': 'Nick'
        }
    }
    return data


@pytest.fixture()
def filter_data():
    data = {
        'form_result_id': 1,
        'user_id': 1,
        'form_id': 1,
        'created': '2020-03-23 22:42:02.614691+02',
        'answers': {
            'name': 'Nick'
        }
    }
    return data


@mock.patch('app.helper.redis_manager.RedisManager.delete')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.DB.session.add')
def test_create(db_mock, redis_get_mock, redis_delete_mock, answer_data):
    instance = FormResult(**answer_data)
    db_mock.return_value = None
    redis_get_mock.return_value = instance
    redis_delete_mock.return_value = None

    test_instance = FormResultService.create(**answer_data)

    assert instance.user_id == test_instance.user_id
    assert instance.form_id == test_instance.form_id
    assert instance.answers == test_instance.answers


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormResult.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id_not_cached(get_mock, query, set_mock, answer_data):
    form_result_id = 1

    instance = FormResult(**answer_data)
    get_mock.return_value = None
    query.get.return_value = instance
    set_mock.return_value = None

    test_instance = FormResultService.get_by_id(form_result_id)

    assert instance.user_id == test_instance.user_id
    assert instance.form_id == test_instance.form_id
    assert instance.answers == test_instance.answers


@mock.patch('app.helper.redis_manager.RedisManager.get')
def test_get_by_id_cached(get_mock, answer_data):
    form_result_id = 1

    instance = FormResult(**answer_data)
    get_mock.return_value = instance

    test_instance = FormResultService.get_by_id(form_result_id)

    assert instance.user_id == test_instance.user_id
    assert instance.form_id == test_instance.form_id
    assert instance.answers == test_instance.answers


@mock.patch('app.helper.redis_manager.RedisManager.set')
@mock.patch('app.models.FormResult.query')
@mock.patch('app.helper.redis_manager.RedisManager.get')
@mock.patch('app.helper.redis_manager.RedisManager.generate_key')
def test_filter(key, get, query, set, answer_data, filter_data):
    instance = FormResult(**answer_data)

    key.return_value = 'qwerty'
    get.return_value = None
    query.filter_by.return_value.all.return_value = [instance]
    set.return_value = None

    test_instance = FormResultService.filter(**filter_data)
    test_instance = test_instance[0]

    assert instance.user_id == test_instance.user_id
    assert instance.form_id == test_instance.form_id
    assert instance.answers == test_instance.answers
