import pytest
import mock

from app.helper.redis_manager import RedisManager
from app.models.user import User


@pytest.fixture()
def get_data():
    data = {
        'name': 'test_name',
        'key': 'test_ket'
    }

    return data


@pytest.fixture()
def user_data():
    user = {"username": "ladia","email": "ladi@gmail.com","google_token": "asd21"}
    return user


@pytest.fixture()
def set_data():
    data = {
        'name': 'test_name',
        'instance': 'test_instance'
    }

    return data


@pytest.fixture()
def generate_data():
    data = {
        'basic_name': 'test_name',
        'hash_dict': {
            "username": "ladia",
            "email": "ladi@gmail.com",
            "google_token": "asd21"
        }
    }

    return data


@mock.patch('pickle.loads')
@mock.patch('app.REDIS.hget')
def test_get(get_mock, pickle_mock, user_data, get_data):
    instance = User(**user_data)

    get_mock.return_value = instance
    pickle_mock.return_value = instance

    test_instance = RedisManager.get(**get_data)

    assert instance.username == test_instance.username
    assert instance.email == test_instance.email
    assert instance.google_token == test_instance.google_token


@mock.patch('app.REDIS.hget')
def test_get_not_cached(get_mock, get_data):
    get_mock.return_value = None

    test_instance = RedisManager.get(**get_data)

    assert test_instance == None


@mock.patch('app.REDIS.expire')
@mock.patch('app.REDIS.hset')
def test_set(set, expire, set_data):
    set.return_value = None
    expire.return_value = None
    test = RedisManager.set(**set_data)

    assert test == None


@mock.patch('app.REDIS.delete')
def test_delete(delete):
    delete.return_value = None

    assert RedisManager.delete('name') == None


def test_generate_key(generate_data):
    answer = 'test_nameusername:ladiaemail:ladi@gmail.comgoogle_token:asd21'
    test = RedisManager.generate_key(**generate_data)

    assert answer == test
