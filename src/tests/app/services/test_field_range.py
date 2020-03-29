import pytest
import mock

from app.services import FieldRangeService
from app.models.field_range import FieldRange


@pytest.fixture()
def field_range_data():
    data = {
        'field_id': 1,
        'range_id': 1
    }
    return data


@pytest.fixture()
def field_range_data_with_id():
    data = {
        'id': 1,
        'field_id': 1,
        'range_id': 1
    }
    return data


@pytest.fixture()
def updated_field_range_data_with_id():
    data = {
        'id': 1,
        'field_id': 1,
        'range_id': 2
    }
    return data


@mock.patch('app.DB.session.add')
def test_create(db_mock, field_range_data):
    """
    Create
    """
    db_mock.return_value = None
    instance = FieldRange(**field_range_data)
    test_instance = FieldRangeService.create(**field_range_data)

    assert instance.field_id == test_instance.field_id
    assert instance.range_id == test_instance.range_id


@mock.patch('app.models.FieldRange.query')
def test_get_by_field_id(query_mock, field_range_data):
    """
    Get by field_id
    """
    instance = FieldRange(**field_range_data)

    query_mock.filter_by.return_value.first.return_value = instance
    test_instance = FieldRangeService.get_by_field_id(field_id=field_range_data.get('field_id'))

    assert instance.field_id == test_instance.field_id
    assert instance.range_id == test_instance.range_id


@mock.patch('app.models.FieldRange.query')
def test_get_by_range_id(query_mock, field_range_data):
    """
    Get by range_id
    """
    instance = FieldRange(**field_range_data)

    query_mock.filter_by.return_value.all.return_value = [instance]
    test_instance = FieldRangeService.get_by_range_id(range_id=field_range_data.get('range_id'))

    assert [instance] == test_instance


@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.DB.session.delete')
def test_delete_exist_field(db_mock, service_mock, field_range_data_with_id):
    """
    Successful update
    """

    service_mock.return_value = FieldRange(**field_range_data_with_id)
    db_mock.return_value = None

    delete_result = FieldRangeService.delete(field_range_data_with_id.get('id'))

    assert delete_result is True


@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_delete_not_exist_field(service_mock, field_range_data_with_id):
    """
    Non-existing delete
    """

    service_mock.return_value = None
    delete_result = FieldRangeService.delete(field_range_data_with_id.get('id'))

    assert delete_result is None


@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_update_not_exist_field(service_mock, field_range_data_with_id):
    """
    Non-existing update
    """

    service_mock.return_value = None
    update_result = FieldRangeService.update(field_range_data_with_id.get('id'))

    assert update_result is None


@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.DB.session.merge')
def test_update_exist_field(
        db_mock,
        service_mock,
        field_range_data_with_id,
        updated_field_range_data_with_id):
    """
    Successful update
    """

    service_mock.return_value = FieldRange(**field_range_data_with_id)
    db_mock.return_value = None

    new_range_id = updated_field_range_data_with_id.get('range_id')
    update_result = FieldRangeService.update(field_range_data_with_id.get('id'), new_range_id)

    assert update_result.range_id == updated_field_range_data_with_id.get('range_id')
