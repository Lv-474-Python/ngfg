"""
Test UserService
"""

import mock
import pytest

from app.models import User
from app.services.user import UserService

from .services_test_data import (
    USER_SERVICE_CREATE_WITHOUT_FILTER_DATA,
    USER_SERVICE_CREATE_WITH_FILTER_DATA,
    USER_SERVICE_GET_BY_ID_DATA,
    USER_SERVICE_UPDATE_DATA,
    USER_SERVICE_UPDATE_ERROR_DATA,
    USER_SERVICE_DELETE_DATA,
    USER_SERVICE_DELETE_ERROR_DATA,
    USER_SERVICE_FILTER_BY_USERNAME_DATA,
    USER_SERVICE_FILTER_BY_EMAIL_DATA,
    USER_SERVICE_FILTER_BY_GOOGLE_TOKEN_DATA,
    USER_SERVICE_FILTER_BY_IS_ACTIVE_DATA,
    USER_SERVICE_FILTER_BY_ALL_DATA,
    USER_SERVICE_CREATE_USER_BY_EMAIL_DATA
)


# create
@pytest.mark.parametrize(
    "username, email, google_token",
    USER_SERVICE_CREATE_WITHOUT_FILTER_DATA
)
@mock.patch("app.DB.session.add")
@mock.patch("app.services.UserService.filter")
def test_create_without_filter(
        mock_user_filter,
        mock_db_add,
        username,
        email,
        google_token):
    """
    Test UserService create()
    Test case when UserService.filter() returned None
    """
    user = User(
        username=username,
        email=email,
        google_token=google_token
    )

    mock_user_filter.return_value = None
    mock_db_add.return_value = None

    result = UserService.create(username, email, google_token)

    assert result.username == user.username
    assert result.email == user.email
    assert result.google_token == user.google_token


@pytest.mark.parametrize(
    "username, email, google_token",
    USER_SERVICE_CREATE_WITH_FILTER_DATA
)
@mock.patch("app.services.UserService.filter")
def test_create_with_filter(mock_user_filter, username, email, google_token):
    """
    Test UserService create()
    Test case when UserService.filter() returned users
    """
    user = User(
        username=username,
        email=email,
        google_token=google_token
    )

    mock_user_filter.return_value = [user]

    result = UserService.create(username, email, google_token)

    assert result.username == user.username
    assert result.email == user.email
    assert result.google_token == user.google_token


# get_by_id
@pytest.mark.parametrize(
    "user_id, username, email, google_token",
    USER_SERVICE_GET_BY_ID_DATA
)
@mock.patch("app.models.User.query")
def test_get_by_id(mock_user_query, user_id, username, email, google_token):
    """
    Test UserService get_by_id()
    Test case when method executed successfully
    """
    user = User(
        username=username,
        email=email,
        google_token=google_token
    )

    mock_user_query.get.return_value = user

    result = UserService.get_by_id(user_id)

    assert result.username == user.username
    assert result.email == user.email
    assert result.google_token == user.google_token


# update
@pytest.fixture()
def user():
    user = User(
        username="ladia",
        email="ladi@gmail.com",
        google_token="asd21"
    )
    return user


@pytest.mark.parametrize(
    "user_id, username, email, google_token, is_active ",
    USER_SERVICE_UPDATE_DATA
)
@mock.patch("app.DB.session.merge")
@mock.patch("app.services.UserService.get_by_id")
def test_update(
        mock_user_get,
        mock_db_merge,
        user,
        user_id,
        username,
        email,
        google_token,
        is_active):
    """
    Test UserService update()
    Test case when method executed successfully
    """
    mock_user_get.return_value = user
    mock_db_merge.return_value = None

    updated_username = username if username is not None else user.username
    updated_email = email if email is not None else user.email
    updated_google_token = google_token if google_token is not None else user.google_token
    updated_is_active = is_active if is_active is not None else user.is_active

    result = UserService.update(user_id, username, email, google_token, is_active)

    assert result.username == updated_username
    assert result.email == updated_email
    assert result.google_token == updated_google_token
    assert result.is_active == updated_is_active


@pytest.mark.parametrize(
    "user_id",
    USER_SERVICE_UPDATE_ERROR_DATA
)
@mock.patch("app.services.UserService.get_by_id")
def test_update_error(mock_user_get, user_id):
    """
    Test UserService update()
    Test case when method raised UserNotExist and returned None
    """
    mock_user_get.return_value = None

    result = UserService.update(user_id)

    assert result is None


# delete
@pytest.mark.parametrize(
    "user_id",
    USER_SERVICE_DELETE_DATA
)
@mock.patch("app.DB.session.delete")
@mock.patch("app.services.UserService.get_by_id")
def test_delete(mock_user_get, mock_db_delete, user, user_id):
    """
    Test UserService delete()
    Test case when method executed successfully
    """
    mock_user_get.return_value = user
    mock_db_delete.return_value = None

    result = UserService.delete(user_id)

    assert result == True


@pytest.mark.parametrize(
    "user_id",
    USER_SERVICE_DELETE_ERROR_DATA
)
@mock.patch("app.services.UserService.get_by_id")
def test_delete_error(mock_user_get, user_id):
    """
    Test UserService delete()
    Test case when method raised UserNotExist and returned None
    """
    mock_user_get.return_value = None

    result = UserService.delete(user_id)

    assert result is None


# filter
@pytest.mark.parametrize(
    "username",
    USER_SERVICE_FILTER_BY_USERNAME_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_username(mock_user_query, user, username):
    """
    Test UserService filter()
    Test case when method filtered just by username
    """
    user.username = username

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(username=username)

    assert result == [user]


@pytest.mark.parametrize(
    "email",
    USER_SERVICE_FILTER_BY_EMAIL_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_email(mock_user_query, user, email):
    """
    Test UserService filter()
    Test case when method filtered just by email
    """
    user.email = email

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(email=email)

    assert result == [user]


@pytest.mark.parametrize(
    "google_token",
    USER_SERVICE_FILTER_BY_GOOGLE_TOKEN_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_google_token(mock_user_query, user, google_token):
    """
    Test UserService filter()
    Test case when method filtered just by google_token
    """
    user.google_token = google_token

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(google_token=google_token)

    assert result == [user]


@pytest.mark.parametrize(
    "is_active",
    USER_SERVICE_FILTER_BY_IS_ACTIVE_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_is_active(mock_user_query, user, is_active):
    """
    Test UserService filter()
    Test case when method filtered just by is_active
    """
    user.is_active = is_active

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(is_active=is_active)

    assert result == [user]


@pytest.mark.parametrize(
    "username, email, google_token, is_active",
    USER_SERVICE_FILTER_BY_ALL_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_all(
        mock_user_query,
        user,
        username,
        email,
        google_token,
        is_active):
    """
    Test UserService filter()
    Test case when method filtered by username, email, google_token, is_active
    """
    user = User(
        username=username,
        email=email,
        google_token=google_token,
        is_active=is_active
    )

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(
        username=username,
        email=email,
        google_token=google_token,
        is_active=is_active
    )

    assert result == [user]


@pytest.mark.parametrize(
    "email",
    USER_SERVICE_CREATE_USER_BY_EMAIL_DATA
)
@mock.patch('app.DB.session.add')
@mock.patch('app.services.UserService.filter')
def test_create_user_by_email(filter_mock, add_mock, email):
    """
    Test UserService create_user_by_email()
    Test case when method executed successfully
    """
    user = User(email=email)
    filter_mock.return_value = None
    add_mock.return_value = None

    result = UserService.create_user_by_email(email)

    assert result == user


@pytest.mark.parametrize(
    "email",
    USER_SERVICE_CREATE_USER_BY_EMAIL_DATA
)
@mock.patch('app.DB.session.add')
@mock.patch('app.services.UserService.filter')
def test_create_user_by_email_user_exist(filter_mock, add_mock, email):
    """
        Test UserService create_user_by_email()
        Test case when filter returned list of objects and method returns [0] of it
    """
    user = User(email=email)
    filter_mock.return_value = [user]
    add_mock.return_value = None

    result = UserService.create_user_by_email(email)

    assert result == user


@pytest.mark.parametrize(
    "email",
    USER_SERVICE_CREATE_USER_BY_EMAIL_DATA
)
@mock.patch('app.services.UserService.create_user_by_email')
def test_create_users_by_emails(create_user_by_email_mock, email):
    """
        Test UserService create_user_by_emails()
        Test case when method executed successfully
    """
    user = User(email=email)
    create_user_by_email_mock.return_value = user

    result = UserService.create_users_by_emails([email])

    assert result == [user]


@pytest.mark.parametrize(
    "email",
    USER_SERVICE_CREATE_USER_BY_EMAIL_DATA
)
@mock.patch('app.services.UserService.create_user_by_email')
def test_create_users_by_emails_user_not_created(create_user_by_email_mock, email):
    """
        Test UserService create_user_by_email()
        Test case when method raised UserNotCreated and returned None
    """
    create_user_by_email_mock.return_value = None

    result = UserService.create_users_by_emails([email])

    assert result == None
