import pytest
import mock

from app.services import GroupService
from app.models import Group, GroupUser, User


@pytest.fixture
def user():
    data = {
        'id': 1,
        'email': 'test_email@gmail.com',
        'username': 'test',
        'google_token': 'test_google_token',
        'is_active': True
    }
    return User(**data)


@pytest.fixture
def group_user():
    data = {
        'user_id': 1,
        'group_id': 1
    }

    return GroupUser(**data)


@pytest.fixture
def group():
    data = {
        'id': 4,
        'name': 'TestGroup',
        'owner_id': 1
    }
    return Group(**data)


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


@mock.patch('app.services.GroupUserService.delete_by_group_and_user_id')
@mock.patch('app.services.GroupUserService.filter')
@mock.patch('app.services.UserService.filter')
def test_unsign_user_by_emails_success(
        user_service_filter_mock,
        group_user_filter_mock,
        group_user_delete_mock,
        group,
        user,
        group_user):
    user_service_filter_mock.return_value = [user]
    group_user_delete_mock.return_value = True
    group_user_filter_mock.return_value = [group_user]

    result = GroupService.unsign_users_by_email(group.id, [user.email])

    assert result is True


@mock.patch('app.services.UserService.filter')
def test_unsign_user_by_emails_user_not_exist(
        user_service_filter_mock,
        group,
        user):
    user_service_filter_mock.return_value = []
    result = GroupService.unsign_users_by_email(group.id, [user.email])

    assert result is None


@mock.patch('app.services.GroupUserService.filter')
@mock.patch('app.services.UserService.filter')
def test_unsign_user_by_emails_user_not_in_group(
        user_service_filter_mock,
        group_user_filter_mock,
        group,
        user):
    user_service_filter_mock.return_value = [user]
    group_user_filter_mock.return_value = []

    result = GroupService.unsign_users_by_email(group.id, [user.email])

    assert result is None


@mock.patch('app.services.GroupService.unsign_users_by_email')
@mock.patch('app.services.GroupService.assign_users_to_group')
@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.update')
@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_success(
        group_get_by_id_mock,
        group_update_mock,
        user_create_user_by_emails_mock,
        group_assign_users_mock,
        group_unsign_users_mock,
        group,
        user,
        group_user):
    group_get_by_id_mock.return_value = group
    group_update_mock.return_value = group
    user_create_user_by_emails_mock.return_value = [user]
    group_assign_users_mock.return_value = [group_user]
    group_unsign_users_mock.return_value = True

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is True


@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_group_not_exist(
        group_get_by_id_mock,
        group,
        user):
    group_get_by_id_mock.return_value = None

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is None


@mock.patch('app.services.GroupService.update')
@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_group_name_already_exist(
        group_get_by_id_mock,
        group_update_mock,
        group,
        user):
    group_get_by_id_mock.return_value = group
    group_update_mock.return_value = None

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is None


@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.update')
@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_not_create_new_users(
        group_get_by_id_mock,
        group_update_mock,
        user_create_user_by_emails_mock,
        group,
        user):
    group_get_by_id_mock.return_value = group
    group_update_mock.return_value = group
    user_create_user_by_emails_mock.return_value = None

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is None


@mock.patch('app.services.GroupService.assign_users_to_group')
@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.update')
@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_not_assigned_new_users(
        group_get_by_id_mock,
        group_update_mock,
        user_create_user_by_emails_mock,
        group_assign_users_mock,
        group,
        user):
    group_get_by_id_mock.return_value = group
    group_update_mock.return_value = group
    user_create_user_by_emails_mock.return_value = [user]
    group_assign_users_mock.return_value = None

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is None


@mock.patch('app.services.GroupService.unsign_users_by_email')
@mock.patch('app.services.GroupService.assign_users_to_group')
@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.update')
@mock.patch('app.services.GroupService.get_by_id')
def test_update_group_and_users_not_unsigned_old_users(
        group_get_by_id_mock,
        group_update_mock,
        user_create_user_by_emails_mock,
        group_assign_users_mock,
        group_unsign_users_mock,
        group,
        user,
        group_user):
    group_get_by_id_mock.return_value = group
    group_update_mock.return_value = group
    user_create_user_by_emails_mock.return_value = [user]
    group_assign_users_mock.return_value = [group_user]
    group_unsign_users_mock.return_value = False

    result = GroupService.update_group_name_and_users(
        group.id,
        [user.email],
        [user.email],
        group.name
    )

    assert result is None


@mock.patch('app.services.GroupService.get_users_by_group')
@mock.patch('app.services.GroupService.to_json')
def test_to_json_single(
        group_to_json_mock,
        group_get_user_mock,
        group,
        user
):
    group_to_json_mock.return_value = {
        'name': group.name,
        'id': group.id,
        'ownerId': group.owner_id,
        'created': None
    }
    group_get_user_mock.return_value = [
        {
            'username': user.username,
            'isActive': user.is_active,
            'id': user.id,
            'email': user.email
        }
    ]

    data = {
        'name': group.name,
        'id': group.id,
        'ownerId': group.owner_id,
        'created': None,
        'users': [{
            'username': user.username,
            'isActive': user.is_active,
            'id': user.id,
            'email': user.email
        }]
    }
    result = GroupService.to_json_single(group)
    assert result == data


@mock.patch('app.services.GroupService.assign_users_to_group')
@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.create')
def test_create_group_with_users(
        create_mock,
        user_create_user_by_emails_mock,
        group_assign_users_mock,
        group, user,
        group_user):
    create_mock.return_value = group
    user_create_user_by_emails_mock.return_value = [user]
    group_assign_users_mock.return_value = [group_user]

    test_instance = GroupService.create_group_with_users(
        group_name=group.name,
        group_owner_id=group.owner_id,
        emails=[user.email]
    )

    assert test_instance == group


@mock.patch('app.services.GroupService.create')
def test_create_group_with_users_group_not_created(
        create_mock,
        group, user):
    create_mock.return_value = None

    test_instance = GroupService.create_group_with_users(
        group_name=group.name,
        group_owner_id=group.owner_id,
        emails=[user.email]
    )

    assert test_instance is None


@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.create')
def test_create_group_with_users_user_not_created(
        create_mock,
        user_create_user_by_emails_mock,
        group,
        user):
    create_mock.return_value = group
    user_create_user_by_emails_mock.return_value = None

    test_instance = GroupService.create_group_with_users(
        group_name=group.name,
        group_owner_id=group.owner_id,
        emails=[user.email]
    )

    assert test_instance is None


@mock.patch('app.services.GroupService.assign_users_to_group')
@mock.patch('app.services.UserService.create_users_by_emails')
@mock.patch('app.services.GroupService.create')
def test_create_group_with_users_group_user_not_created(
        create_mock,
        user_create_user_by_emails_mock,
        group_assign_users_mock,
        group, user):
    create_mock.return_value = group
    user_create_user_by_emails_mock.return_value = [user]
    group_assign_users_mock.return_value = None

    test_instance = GroupService.create_group_with_users(
        group_name=group.name,
        group_owner_id=group.owner_id,
        emails=[user.email]
    )

    assert test_instance is None


@mock.patch('app.services.GroupUserService.create')
def test_assign_users_to_group(create_mock, group_user, user):
    create_mock.return_value = group_user

    test_instance = GroupService.assign_users_to_group(group_user.id, [user])

    assert test_instance == [group_user]


@mock.patch('app.services.GroupUserService.create')
def test_assign_users_to_group_raised_group_user_not_created(create_mock, group_user, user):
    create_mock.return_value = None

    test_instance = GroupService.assign_users_to_group(group_user.id, [user])

    assert test_instance is None
