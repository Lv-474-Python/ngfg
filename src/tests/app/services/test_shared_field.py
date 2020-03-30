import pytest
import mock

from app.models import SharedField
from app.services import SharedFieldService


@pytest.fixture()
def shared_field_data():
    data = {
        'owner_id': 1,
        'user_id': 2,
        'field_id': 1
    }
    return data


@pytest.fixture()
def shared_field_data_with_id():
    data = {
        'id': 1,
        'owner_id': 1,
        'user_id': 2,
        'field_id': 1
    }
    return data


@mock.patch('app.DB.session.add')
def test_create(db_mock, shared_field_data):

    db_mock.return_value = None
    instance = SharedField(**shared_field_data)
    test_instance = SharedFieldService.create(**shared_field_data)

    assert instance.owner_id == test_instance.owner_id
    assert instance.field_id == test_instance.field_id
    assert instance.user_id == test_instance.user_id


@mock.patch('app.models.SharedField.query')
def test_get_by_id(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.get.return_value = instance
    test_instance = SharedFieldService.get_by_id(instance.id)

    assert instance.owner_id == test_instance.owner_id
    assert instance.field_id == test_instance.field_id
    assert instance.user_id == test_instance.user_id


@mock.patch('app.models.SharedField.query')
def test_filter_by_owner_id(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SharedFieldService.filter(owner_id=instance.owner_id)
    test_instance = test_list[0]

    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.models.SharedField.query')
def test_filter_by_user_id(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SharedFieldService.filter(user_id=instance.user_id)
    test_instance = test_list[0]

    assert instance.user_id == test_instance.user_id


@mock.patch('app.models.SharedField.query')
def test_filter_by_field_id(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SharedFieldService.filter(field_id=instance.field_id)
    test_instance = test_list[0]

    assert instance.field_id == test_instance.field_id


@mock.patch('app.models.SharedField.query')
def test_filter_by_shared_field_id(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SharedFieldService.filter(shared_field_id=1)
    test_instance = test_list[0]

    assert instance.id == test_instance.id


@mock.patch('app.models.SharedField.query')
def test_filter_by_all(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SharedFieldService.filter(
        owner_id=instance.field_id,
        user_id=instance.user_id,
        field_id=instance.field_id
    )
    test_instance = test_list[0]

    assert instance.field_id == test_instance.field_id
    assert instance.user_id == test_instance.user_id
    assert instance.owner_id == test_instance.owner_id


@mock.patch('app.services.SharedFieldService.get_by_id')
@mock.patch('app.DB.session.delete')
def test_delete_exist_field(db_mock, shared_field_service_mock, shared_field_data_with_id):
    shared_field_service_mock.return_value = SharedField(**shared_field_data_with_id)
    db_mock.return_value = None

    delete_result = SharedFieldService.delete(shared_field_data_with_id.get('id'))

    assert delete_result is True


@mock.patch('app.services.SharedFieldService.get_by_id')
def test_delete_not_exist_field(shared_field_service_mock, shared_field_data_with_id):
    shared_field_service_mock.return_value = None
    delete_result = SharedFieldService.delete(shared_field_data_with_id.get('id'))

    assert delete_result is None


@mock.patch('app.models.SharedField.query')
def test_get_by_user_and_field(query, shared_field_data):
    instance = SharedField(**shared_field_data)

    query.filter_by.return_value.first.return_value = instance
    test_instance = SharedFieldService.get_by_user_and_field(
        user_id=instance.user_id,
        field_id=instance.field_id
    )

    assert instance.field_id == test_instance.field_id
    assert instance.user_id == test_instance.user_id


@mock.patch('app.schemas.SharedFieldPostSchema')
def test_validate_post_data(schema, shared_field_data_with_id):
    instance = SharedField(**shared_field_data_with_id)
    schema.validate.return_value = instance

    result, errors = SharedFieldService.validate_post_data(instance)

    assert not result
    assert errors == {'_schema': ['Invalid input type.']}


@mock.patch('app.schemas.SharedFieldPostSchema')
def test_to_json(schema):
    schema.return_value = None
    result = SharedFieldService.to_json(None, many=False)
    assert result == {}


@mock.patch('app.schemas.SharedFieldResponseSchema')
def test_response_to_json(schema):
    schema.return_value = None
    result = SharedFieldService.response_to_json(None, many=False)
    assert result == {}
