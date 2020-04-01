import pytest
import mock
from sqlalchemy.exc import (
    IntegrityError,
    ProgrammingError,
    SQLAlchemyError
)

from app.helper.errors import CustomException
from app.services import FieldService


@mock.patch('app.helper.decorators.LOGGER')
@mock.patch('app.DB.session.add')
def test_decorator_custom_error(db_mock, logger_mock):
    db_mock.side_effect = mock.Mock(side_effect=CustomException())
    test_instance = FieldService.create(name='name',
                                        owner_id=1,
                                        field_type=1)

    assert test_instance is None
    assert logger_mock.error.called is True


@pytest.fixture()
def exception_data():
    data = {'statement': 1, 'params': 1, 'orig': 1}
    return data


@mock.patch('app.helper.decorators.LOGGER')
@mock.patch('app.DB.session.add')
def test_decorator_integrity_error(db_mock, logger_mock, exception_data):
    db_mock.side_effect = mock.Mock(side_effect=IntegrityError(**exception_data))
    test_instance = FieldService.create(name='name',
                                        owner_id=1,
                                        field_type=1)

    assert test_instance is None
    assert logger_mock.error.called is True


@mock.patch('app.helper.decorators.LOGGER')
@mock.patch('app.DB.session.add')
def test_decorator_programming_error(db_mock, logger_mock, exception_data):
    db_mock.side_effect = mock.Mock(side_effect=ProgrammingError(**exception_data))
    test_instance = FieldService.create(name='name',
                                        owner_id=1,
                                        field_type=1)

    assert test_instance is None
    assert logger_mock.error.called is True


@mock.patch('app.helper.decorators.LOGGER')
@mock.patch('app.DB.session.add')
def test_decorator_sql_alchemy_error(db_mock, logger_mock):
    db_mock.side_effect = mock.Mock(side_effect=SQLAlchemyError())
    test_instance = FieldService.create(name='name',
                                        owner_id=1,
                                        field_type=1)

    assert test_instance is None
    assert logger_mock.error.called is True
