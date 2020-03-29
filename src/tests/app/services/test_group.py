import pytest
import mock

from app.models import Group, User, GroupUser
from app.services import GroupService


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