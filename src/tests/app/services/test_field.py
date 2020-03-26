import pytest
import mock

from app.services import FieldService
from app.models.field import Field


@pytest.fixture()
def field_data():
    data = {
        'name': 'TestFieldName1',
        'owner_id': 1,
        'field_type': 1,
        'is_strict': False
    }
    return data


@pytest.fixture()
def field_data_with_id():
    data = {
        'id': 1,
        'name': 'TestFieldName1',
        'owner_id': 1,
        'field_type': 1,
        'is_strict': False
    }
    return data


@mock.patch('app.DB.session.add')
def test_create(db_mock, field_data):

    db_mock.return_value = None
    instance = Field(**field_data)
    test_instance = FieldService.create(**field_data)

    assert instance.name == test_instance.name
    assert instance.owner_id == test_instance.owner_id
    assert instance.field_type == test_instance.field_type
    assert instance.is_strict == test_instance.is_strict


@mock.patch('app.models.Field.query')
def test_get_by_id(query, field_data):
    instance = Field(**field_data)

    query.get.return_value = instance
    test_instance = FieldService.get_by_id(1)

    assert instance.name == test_instance.name
    assert instance.owner_id == test_instance.owner_id
    assert instance.field_type == test_instance.field_type
    assert instance.is_strict == test_instance.is_strict


@mock.patch('app.models.Field.query')
def test_filter_by_name(query, field_data):
    instance = Field(**field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(name=field_data.get('name'))
    test_instance = test_list[0]

    assert instance.name == test_instance.name


@mock.patch('app.models.Field.query')
def test_filter_by_owner_id(query, field_data):
    instance = Field(**field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(owner_id=field_data.get('owner_id'))
    test_instance = test_list[0]

    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.models.Field.query')
def test_filter_by_field_type(query, field_data):
    instance = Field(**field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(field_type=field_data.get('field_type'))
    test_instance = test_list[0]

    assert instance.field_type == test_instance.field_type


@mock.patch('app.models.Field.query')
def test_filter_by_is_strict(query, field_data):
    instance = Field(**field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(is_strict=field_data.get('is_strict'))
    test_instance = test_list[0]

    assert instance.is_strict == test_instance.is_strict


@mock.patch('app.models.Field.query')
def test_filter_by_id(query, field_data_with_id):
    instance = Field(**field_data_with_id)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(field_id=field_data_with_id.get('id'))
    test_instance = test_list[0]

    assert instance.id == test_instance.id


@mock.patch('app.models.Field.query')
def test_filter_by_all(query, field_data_with_id):
    instance = Field(**field_data_with_id)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = FieldService.filter(
        field_id=field_data_with_id.get('id'),
        name=field_data_with_id.get('name'),
        owner_id=field_data_with_id.get('owner_id'),
        field_type=field_data_with_id.get('field_type'),
        is_strict=field_data_with_id.get('is_strict')
    )
    test_instance = test_list[0]

    assert instance.id == test_instance.id
    assert instance.name == test_instance.name
    assert instance.owner_id == test_instance.owner_id
    assert instance.field_type == test_instance.field_type
    assert instance.is_strict == test_instance.is_strict


@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.DB.session.delete')
def test_delete_exist_field(db_mock, field_service_mock, field_data_with_id):
    field_service_mock.return_value = Field(**field_data_with_id)
    db_mock.return_value = None

    delete_result = FieldService.delete(field_data_with_id.get('id'))

    assert delete_result is True


@mock.patch('app.services.FieldService.get_by_id')
def test_delete_not_exist_field(field_service_mock, field_data_with_id):
    field_service_mock.return_value = None
    delete_result = FieldService.delete(field_data_with_id.get('id'))

    assert delete_result is None


@mock.patch('app.services.FieldService.get_by_id')
def test_update_not_exist_field(field_service_mock, field_data_with_id):
    field_service_mock.return_value = None
    update_result = FieldService.update(field_id=field_data_with_id.get('id'))

    assert update_result is None


@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_field_name(db_mock, field_service_mock, field_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'UpdatedTestFieldName1',
        'owner_id': 1,
        'field_type': 1,
        'is_strict': False
    }
    instance = Field(**field_data_with_id)
    updated_instance = Field(**updated_data)

    field_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = FieldService.update(
        field_id=field_data_with_id.get('id'),
        name=updated_data.get('name')
    )

    assert updated_instance.name == update_result.name


@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_field_owner_id(db_mock, field_service_mock, field_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'TestFieldName1',
        'owner_id': 2,
        'field_type': 1,
        'is_strict': False
    }
    instance = Field(**field_data_with_id)
    updated_instance = Field(**updated_data)

    field_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = FieldService.update(
        field_id=field_data_with_id.get('id'),
        owner_id=updated_data.get('owner_id')
    )

    assert updated_instance.owner_id == update_result.owner_id


@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_field_field_type(db_mock, field_service_mock, field_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'TestFieldName1',
        'owner_id': 1,
        'field_type': 2,
        'is_strict': False
    }
    instance = Field(**field_data_with_id)
    updated_instance = Field(**updated_data)

    field_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = FieldService.update(
        field_id=field_data_with_id.get('id'),
        field_type=updated_data.get('field_type')
    )

    assert updated_instance.field_type == update_result.field_type


@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update_field_is_strict(db_mock, field_service_mock, field_data_with_id):
    updated_data = {
        'id': 1,
        'name': 'TestFieldName1',
        'owner_id': 1,
        'field_type': 1,
        'is_strict': True
    }
    instance = Field(**field_data_with_id)
    updated_instance = Field(**updated_data)

    field_service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = FieldService.update(
        field_id=field_data_with_id.get('id'),
        is_strict=updated_data.get('is_strict')
    )

    assert updated_instance.is_strict == update_result.is_strict
