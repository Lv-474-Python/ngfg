import pytest
from app.models import User, Group
from flask import jsonify
import mock
from app import APP, DB
import json


@pytest.fixture
def user():
    data = {
        'id': 1,
        'username': 'test',
        'email': "test@gmail.com",
        'google_token': 'test_google_token',
        'is_active': True
    }
    return User(**data)


@pytest.fixture
def group():
    data = {
        'id': 1,
        'name': 'TestGroup',
        'owner_id': 1
    }
    return Group(**data)


@pytest.fixture
def headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers


@pytest.fixture
def group_json(group, user):
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

    return data


@pytest.fixture
def basic_group_json(group):
    data = {
        'name': group.name,
        'owner_id': group.owner_id,
        'id': group.id,
        'created': group.created
    }
    return data


@pytest.fixture
def group_create_json(group, user):
    data = {
        'name': group.name,
        'usersEmails': [
            user.email
        ]
    }

    return data


@pytest.fixture
def group_put_data():
    data = {
        'name': 'TestGroup',
        'emailsAdd': [],
        'emailsDelete': []
    }
    return data


@pytest.fixture
def client(user):
    APP.config['TESTING'] = True
    APP.config['WTF_CSRF_ENABLED'] = False
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    testing_client = APP.test_client()

    ctx = APP.app_context()
    ctx.push()

    with testing_client.session_transaction() as session:
        session['_user_id'] = user.id

    yield testing_client

    ctx.pop()


@mock.patch('app.services.GroupService.to_json_all')
@mock.patch('app.services.GroupService.filter')
def test_groups_get_all(group_filter_mock, group_to_json_all_mock, client, group, group_json):
    group_filter_mock.return_value = [group]
    group_to_json_all_mock.return_value = [group_json]

    response = client.get('api/v1/groups', follow_redirects=True)
    assert response.status_code == 200
    assert response.data == jsonify({'groups': [group_json]}).data


@mock.patch('app.services.GroupService.to_json_single')
@mock.patch('app.services.GroupService.create_group_with_users')
@mock.patch('app.services.GroupService.validate_post_data')
def test_groups_post(
        validate_post_mock,
        create_group_mock,
        to_json_mock,
        client,
        group,
        group_json,
        group_create_json,
        headers):
    validate_post_mock.return_value = (True, [])
    create_group_mock.return_value = group
    to_json_mock.return_value = group_json

    response = client.post(
        '/api/v1/groups',
        data=json.dumps(group_create_json),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 201
    assert response.data == jsonify(group_json).data


@mock.patch('app.services.GroupService.validate_post_data')
def test_groups_post_validate_not_passed(
        validate_post_mock,
        client,
        group_create_json,
        headers):

    validate_post_mock.return_value = (False, ["error"])
    response = client.post(
        '/api/v1/groups',
        data=json.dumps(group_create_json),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 400


@mock.patch('app.services.GroupService.create_group_with_users')
@mock.patch('app.services.GroupService.validate_post_data')
def test_groups_post_group_not_created(
        validate_post_mock,
        create_group_mock,
        client,
        group_create_json,
        headers):
    validate_post_mock.return_value = (True, [])
    create_group_mock.return_value = None

    response = client.post(
        '/api/v1/groups',
        data=json.dumps(group_create_json),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 400


@mock.patch('app.services.GroupService.to_json_single')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_get_one(group_get_by_id_mock, group_to_json_single_mock, client, group, group_json):
    group_get_by_id_mock.return_value = group
    group_to_json_single_mock.return_value = group_json

    response = client.get(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 200
    assert response.data == jsonify(group_json).data


@mock.patch('app.services.GroupService.get_by_id')
def test_groups_get_one_not_found(group_get_by_id_mock, client, group):
    group_get_by_id_mock.return_value = None

    response = client.get(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 400


@mock.patch('app.services.GroupService.delete')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_delete(group_get_by_id_mock, group_delete_mock, client, user, group):
    group_get_by_id_mock.return_value = group
    group_delete_mock.return_value = True
    group.user = user

    response = client.delete(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 204


@mock.patch('app.services.GroupService.get_by_id')
def test_groups_delete_group_not_found(group_get_by_id_mock, client, group):
    group_get_by_id_mock.return_value = None

    response = client.delete(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 400


@mock.patch('app.services.GroupService.delete')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_delete_group_not_deleted(group_get_by_id_mock, group_delete_mock, client, user, group):
    group_get_by_id_mock.return_value = group
    group_delete_mock.return_value = False
    group.user = user

    response = client.delete(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 400


@mock.patch('app.services.GroupService.get_by_id')
def test_groups_delete_not_owner(group_get_by_id_mock, client, group):
    group_get_by_id_mock.return_value = group
    group.user = None

    response = client.delete(f'api/v1/groups/{group.id}', follow_redirects=True)
    assert response.status_code == 403


@mock.patch('app.services.GroupService.to_json_single')
@mock.patch('app.services.GroupService.update_group_name_and_users')
@mock.patch('app.services.GroupService.validate_put_data')
@mock.patch('app.services.GroupService.to_json')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put(
        get_by_id_mock,
        to_json_mock,
        validate_put_mock,
        update_group_mock,
        to_json_single_mock,
        client,
        group_json,
        group,
        basic_group_json,
        group_put_data,
        headers):
    get_by_id_mock.return_value = group
    to_json_mock.return_value = basic_group_json
    validate_put_mock.return_value = (True, [])
    update_group_mock.return_value = group
    to_json_single_mock.return_value = group_json

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps(group_put_data),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert response.data == jsonify(group_json).data


@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put_group_not_exist(
        get_by_id_mock,
        client,
        group_json,
        group,
        group_put_data,
        headers):
    get_by_id_mock.return_value = None

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps(group_put_data),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 400


@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put_not_owner(
        get_by_id_mock,
        client,
        group_json,
        group,
        group_put_data,
        headers):
    group.owner_id = 2
    get_by_id_mock.return_value = group

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps(group_put_data),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 400


@mock.patch('app.services.GroupService.validate_put_data')
@mock.patch('app.services.GroupService.to_json')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put_not_valid_data(
        get_by_id_mock,
        to_json_mock,
        validate_put_mock,
        client,
        group_json,
        group,
        basic_group_json,
        group_put_data,
        headers):
    get_by_id_mock.return_value = group
    to_json_mock.return_value = basic_group_json
    validate_put_mock.return_value = (False, ['error'])

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps(group_put_data),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 400


@mock.patch('app.services.GroupService.update_group_name_and_users')
@mock.patch('app.services.GroupService.validate_put_data')
@mock.patch('app.services.GroupService.to_json')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put_not_update_group(
        get_by_id_mock,
        to_json_mock,
        validate_put_mock,
        update_group_mock,
        client,
        group_json,
        group,
        basic_group_json,
        group_put_data,
        headers):

    get_by_id_mock.return_value = group
    to_json_mock.return_value = basic_group_json
    validate_put_mock.return_value = (True, [])
    update_group_mock.return_value = None

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps(group_put_data),
        headers=headers,
        follow_redirects=True)

    assert response.status_code == 400


@mock.patch('app.services.GroupService.to_json_single')
@mock.patch('app.services.GroupService.update_group_name_and_users')
@mock.patch('app.services.GroupService.validate_put_data')
@mock.patch('app.services.GroupService.to_json')
@mock.patch('app.services.GroupService.get_by_id')
def test_groups_put_without_json_params(
        get_by_id_mock,
        to_json_mock,
        validate_put_mock,
        update_group_mock,
        to_json_single_mock,
        client,
        group_json,
        group,
        basic_group_json,
        headers):
    get_by_id_mock.return_value = group
    to_json_mock.return_value = basic_group_json
    validate_put_mock.return_value = (True, [])
    update_group_mock.return_value = group
    to_json_single_mock.return_value = group_json

    response = client.put(
        f'/api/v1/groups/{group.id}',
        data=json.dumps({'name': 'TestGroup'}),
        headers=headers,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert response.data == jsonify(group_json).data
