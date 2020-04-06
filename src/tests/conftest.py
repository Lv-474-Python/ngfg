import pytest
import mock
from app import APP, DB
from app.models import User


@pytest.fixture()
def login_user():
    data = {
        'id': 1,
        'username': 'test',
        'email': "test@gmail.com",
        'google_token': 'test_google_token',
        'is_active': True
    }
    return User(**data)


@pytest.fixture()
def app(login_user):
    APP.config['TESTING'] = True
    APP.config['WTF_CSRF_ENABLED'] = False
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    query = mock.MagicMock('app.models.User.query')
    query = query()
    query.get.return_value = login_user
    DB.create_all()
    DB.session.add(login_user)

    yield APP
    DB.drop_all()


@pytest.fixture
def client(login_user, app):
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    with testing_client.session_transaction() as session:
        session['_user_id'] = login_user.id

    yield testing_client

    ctx.pop()
