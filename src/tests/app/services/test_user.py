"""
Test UserService
"""


# ЩОБ ВСЮДИ ДЕ None було 'is None'



import mock
import pytest

from app.models import User
from app.services.user import UserService


# create
USER_SERVICE_CREATE_WITHOUT_FILTER_DATA = [
    ("kaic", "kaic@gmail.com", "asdsadaa"),
    ("lsoa", "lsoa@gmail.com", "2fas2af")
]

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

    assert user.username == result.username
    assert user.email == result.email
    assert user.google_token == result.google_token


USER_SERVICE_CREATE_WITH_FILTER_DATA = [
    ("kaic", "kaic@gmail.com", "asdsadaa"),
    ("lsoa", "lsoa@gmail.com", "2fas2af")
]

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

    assert user.username == result.username
    assert user.email == result.email
    assert user.google_token == result.google_token


# get_by_id
USER_SERVICE_GET_BY_ID_DATA = [
    (1, "kaidac", "kwqaic@gmail.com", "asdsadaa"),
    (2, "lsodsaa", "lssadoa@gmail.com", "2fas2af")
]

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

    assert user.username == result.username
    assert user.email == result.email
    assert user.google_token == result.google_token


# update
@pytest.fixture()
def user():
    user = User(
        username="ladia",
        email="ladi@gmail.com",
        google_token="asd21"
    )
    return user


USER_SERVICE_UPDATE_DATA = [
    (1, None, None, None, None),
    (2, "lsodsaa", None, None, None),
    (3, "laaasqwq", "la3a@gmai.com", None, None),
    (4, "sqqasqwq", "laa@gmai.com", "asda", None),
    (5, "laaajnvvmm", "pos42a@gmai.com", "oda1", True),
]

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

    updated_username = username if username else user.username
    updated_email = email if email else user.email
    updated_google_token = google_token if google_token else user.google_token
    updated_is_active = is_active if is_active else user.is_active

    result = UserService.update(user_id, username, email, google_token, is_active)

    assert updated_username == result.username
    assert updated_email == result.email
    assert updated_google_token == result.google_token
    assert updated_is_active == result.is_active


USER_SERVICE_UPDATE_ERROR_DATA = [1, 2]

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
USER_SERVICE_DELETE_DATA = [1, 2]

@pytest.mark.parametrize(
    "user_id",
    USER_SERVICE_DELETE_DATA
)
@mock.patch("app.DB.session.delete")
@mock.patch("app.services.UserService.get_by_id")
def test_delete(mock_user_get, mock_db_merge, user, user_id):
    """
    Test UserService delete()
    Test case when method executed successfully
    """
    mock_user_get.return_value = user
    mock_db_merge.return_value = None

    result = UserService.delete(user_id)
    assert result == True


USER_SERVICE_DELETE_ERROR_DATA = [1, 2]

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
USER_SERVICE_FILTER_BY_USERNAME_DATA = ["sda", "lsodsaa"]

@pytest.mark.parametrize(
    "username",
    USER_SERVICE_FILTER_BY_USERNAME_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_username(mock_user_query, user, username):
    """
    Test UserService filter()
    Test case when method filter just by username
    """
    user.username = username

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(username=username)

    assert [user] == result


USER_SERVICE_FILTER_BY_EMAIL_DATA = ["sda@gmail.com", "lsodsaa@gmail.com"]

@pytest.mark.parametrize(
    "email",
    USER_SERVICE_FILTER_BY_EMAIL_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_email(mock_user_query, user, email):
    """
    Test UserService filter()
    Test case when method filter just by email
    """
    user.email = email

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(email=email)

    assert [user] == result


USER_SERVICE_FILTER_BY_GOOGLE_TOKEN_DATA = ["sda@gmail.com", "lsodsaa@gmail.com"]

@pytest.mark.parametrize(
    "google_token",
    USER_SERVICE_FILTER_BY_GOOGLE_TOKEN_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_google_token(mock_user_query, user, google_token):
    """
    Test UserService filter()
    Test case when method filter just by google_token
    """
    user.google_token = google_token

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(google_token=google_token)

    assert [user] == result


USER_SERVICE_FILTER_BY_IS_ACTIVE_DATA = [True, False]

@pytest.mark.parametrize(
    "is_active",
    USER_SERVICE_FILTER_BY_IS_ACTIVE_DATA
)
@mock.patch("app.models.User.query")
def test_filter_by_is_active(mock_user_query, user, is_active):
    """
    Test UserService filter()
    Test case when method filter just by is_active
    """
    user.is_active = is_active

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(is_active=is_active)

    assert [user] == result


USER_SERVICE_FILTER_BY_ALL_DATA = [
    ("aasdasda", "ada@gmail.com", "asdsada", True),
    ("gd2as", "adacv@gmail.com", "2asd2", False)
]

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
    Test case when method filter by username, email, google_token, is_active
    """
    user = User(
        username=username,
        email=email,
        google_token=google_token,
        is_active=is_active
    )

    mock_user_query.filter_by().all.return_value = [user]

    result = UserService.filter(is_active=is_active)

    assert [user] == result
