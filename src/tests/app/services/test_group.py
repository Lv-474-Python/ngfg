import pytest
import mock

from app.services import GroupService
from app.models import Group, GroupUser
from app.helper.errors import GroupNotExist


@pytest.fixture()
def group_data():
    data = {'id': 1, 'name': 'string', 'owner_id': 1}
    return data


@pytest.fixture()
def group_user_data():
    user = {'user_id': 1, 'group_id': 1}
    return user


@pytest.fixture()
def user_data():
    user = {'id': 1, "username": "string", "email": "testmail1@gmail.com", "is_active": True}
    return user


@pytest.fixture()
def group_data():
    data = {
        'name': 'GroupName1',
        'owner_id': 1
    }
    return data


@pytest.fixture()
def group_user_data():
    user = {'user_id': 1, 'group_id': 1}
    return user


@pytest.fixture()
def group_data_with_id():
    data = {
        'id': 1,
        'name': 'TestGroupName1',
        'owner_id': 1
    }
    return data


@mock.patch('app.DB.session.add')
def test_create(db_mock, group_data):
    db_mock.return_value = None
    instance = Group(**group_data)
    test_instance = GroupService.create(**group_data)

    assert instance.name == test_instance.name
    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.models.Group.query')
def test_get_by_id(query, group_data_with_id):
    instance = Group(**group_data_with_id)

    query.get.return_value = instance
    test_instance = GroupService.get_by_id(1)

    assert test_instance == instance


@mock.patch('app.models.Group.query')
def test_filter_by_name(query, group_data):
    instance = Group(**group_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupService.filter(name=group_data.get('name'))
    test_instance = test_list[0]

    assert instance.name == test_instance.name


@mock.patch('app.models.Group.query')
def test_filter_by_owner_id(query, group_data):
    instance = Group(**group_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupService.filter(owner_id=group_data.get('owner_id'))
    test_instance = test_list[0]

    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.models.Group.query')
def test_filter_by_id(query, group_data_with_id):
    instance = Group(**group_data_with_id)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupService.filter(group_id=group_data_with_id.get('id'))
    test_instance = test_list[0]

    assert instance.id == test_instance.id


@mock.patch('app.models.Group.query')
def test_filter_by_all(query, group_data_with_id):
    instance = Group(**group_data_with_id)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = GroupService.filter(
        group_id=group_data_with_id.get('id'),
        name=group_data_with_id.get('name'),
        owner_id=group_data_with_id.get('owner_id')
    )
    test_instance = test_list[0]

    assert instance.id == test_instance.id
    assert instance.name == test_instance.name
    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.services.GroupService.get_by_id')
@mock.patch('app.DB.session.delete')
def test_delete_exist_group(db_mock, group_service_mock, group_data_with_id):
    group_service_mock.return_value = Group(**group_data_with_id)
    db_mock.return_value = None

    delete_result = GroupService.delete(group_data_with_id.get('id'))

    assert delete_result is True


@mock.patch('app.services.GroupService.get_by_id')
def test_delete_not_exist_group(group_service_mock, group_data_with_id):
    group_service_mock.return_value = None
    delete_result = GroupService.delete(group_data_with_id.get('id'))

    assert delete_result is None


@mock.patch('app.services.GroupService.get_by_id')
def test_update_not_exist_group(group_service_mock, group_data_with_id):
    group_service_mock.return_value = None
    update_result = GroupService.update(group_id=group_data_with_id.get('id'))

    assert update_result is None


@mock.patch('app.services.GroupService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_group_name(db_mock, group_service_mock, group_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'UpdatedTestGroupName1',
        'owner_id': 1
    }
    instance = Group(**group_data_with_id)
    updated_instance = Group(**updated_data)

    group_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = GroupService.update(
        group_id=group_data_with_id.get('id'),
        name=updated_data.get('name')
    )

    assert updated_instance.name == update_result.name


@mock.patch('app.services.GroupService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_group_owner_id(db_mock, group_service_mock, group_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'TestGroupName1',
        'owner_id': 2
    }
    instance = Group(**group_data_with_id)
    updated_instance = Group(**updated_data)

    group_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = GroupService.update(
        group_id=group_data_with_id.get('id'),
        owner_id=updated_data.get('owner_id')
    )

    assert updated_instance.owner_id == update_result.owner_id


@mock.patch('app.services.UserService.to_json')
@mock.patch('app.services.GroupService.get_by_id')
def test_get_users_by_group(get_by_id_mock, to_json_mock, group_data, group_user_data, user_data):
    group_instance = Group(**group_data)
    group_instance.groups_users = [GroupUser(**group_user_data), GroupUser(**group_user_data)]
    user_json = user_data

    get_by_id_mock.return_value = group_instance
    to_json_mock.return_value = user_json

    test_instance = GroupService.get_users_by_group(1)

    assert [user_json, user_json] == test_instance


@mock.patch('app.services.GroupService.get_by_id')
def test_get_users_by_group_error(get_by_id_mock):
    get_by_id_mock.return_value = None
    test_instance = GroupService.get_users_by_group(1)

    assert test_instance == None
