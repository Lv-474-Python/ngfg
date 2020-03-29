import pytest
import mock

from app.services import GroupUserService
from app.models import Group, GroupUser


@pytest.fixture()
def group_user_data():
    user = {'user_id': 1, 'group_id': 1}
    return user


@mock.patch('app.DB.session.add')
def test_create(db_mock, group_user_data):
    db_mock.return_value = None
    instance = GroupUser(**group_user_data)
    test_instance = GroupUserService.create(**group_user_data)

    assert instance.user_id == test_instance.user_id
    assert instance.group_id == test_instance.group_id


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.GroupUserService.get_by_group_and_user_id')
def test_delete_by_group_and_user_id(mock_get, mock_delete, group_user_data):
    grop_user = GroupUser(**group_user_data)
    mock_get.return_value = grop_user
    mock_delete.return_value = None

    result = GroupUserService.delete_by_group_and_user_id(**group_user_data)

    assert result == True


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.GroupUserService.get_by_group_and_user_id')
def test_delete_by_group_and_user_id_error(mock_get, mock_delete, group_user_data):
    mock_get.return_value = None
    mock_delete.return_value = None

    result = GroupUserService.delete_by_group_and_user_id(**group_user_data)

    assert result == None


@mock.patch('app.models.GroupUser.query')
def test_filter_by_user_id(query, group_user_data):
    instance = GroupUser(**group_user_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupUserService.filter(user_id=group_user_data.get('user_id'))
    test_instance = test_list[0]

    assert instance.user_id == test_instance.user_id


@mock.patch('app.models.GroupUser.query')
def test_filter_by_group_id(query, group_user_data):
    instance = GroupUser(**group_user_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupUserService.filter(group_id=group_user_data.get('group_id'))
    test_instance = test_list[0]

    assert instance.group_id == test_instance.group_id


@mock.patch('app.models.GroupUser.query')
def test_filter_by_all(query, group_user_data):
    instance = GroupUser(**group_user_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupUserService.filter(
        group_id=group_user_data.get('group_id'),
        user_id=group_user_data.get('user_id')
    )
    test_instance = test_list[0]

    assert instance.group_id == test_instance.group_id
    assert instance.user_id == test_instance.user_id


@mock.patch('app.models.GroupUser.query')
def test_get_by_group_and_user_id(query, group_user_data):
    instance = GroupUser(**group_user_data)
    query.filter_by.return_value.all.return_value = [instance]

    test_instance = GroupUserService.get_by_group_and_user_id(**group_user_data)

    assert instance == test_instance


@mock.patch('app.models.GroupUser.query')
def test_get_by_group_and_user_id_error(query, group_user_data):
    query.filter_by.return_value.all.return_value = None

    test_instance = GroupUserService.get_by_group_and_user_id(**group_user_data)

    assert test_instance == None
