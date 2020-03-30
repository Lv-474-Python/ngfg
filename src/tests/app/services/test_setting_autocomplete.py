import pytest
import mock

from app.services import SettingAutocompleteService
from app.models import SettingAutocomplete


@pytest.fixture()
def setting_autocomplete_data():
    data = {
        'data_url': 'https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0',
        'sheet': 'sheet',
        'from_row': 'A1',
        'to_row': 'A10',
        'field_id': 1
    }
    return data


@pytest.fixture()
def setting_autocomplete_data_with_id():
    data = {
        'id': 1,
        'data_url': 'https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0',
        'sheet': 'sheet',
        'from_row': 'A1',
        'to_row': 'A10',
        'field_id': 1
    }
    return data


@mock.patch('app.DB.session.add')
def test_create(db_mock, setting_autocomplete_data):
    db_mock.return_value = None
    instance = SettingAutocomplete(**setting_autocomplete_data)
    test_instance = SettingAutocompleteService.create(**setting_autocomplete_data)

    assert instance.data_url == test_instance.data_url
    assert instance.sheet == test_instance.sheet
    assert instance.from_row == test_instance.from_row
    assert instance.to_row == test_instance.to_row
    assert instance.field_id == test_instance.field_id


@mock.patch('app.services.SettingAutocompleteService.get_by_id')
@mock.patch('app.DB.session.merge')
def test_update(db_mock, service_mock, setting_autocomplete_data_with_id):
    updated_data = {
        'data_url': '2',
        'sheet': '2',
        'from_row': '2',
        'to_row': '2',
        'field_id': 2
    }
    instance = SettingAutocomplete(**setting_autocomplete_data_with_id)
    updated_instance = SettingAutocomplete(**updated_data)

    service_mock.return_value = instance
    db_mock.return_value = updated_instance

    update_result = SettingAutocompleteService.update(
        setting_autocomplete_id=updated_data.get('id'),
        data_url=updated_data.get('data_url'),
        sheet=updated_data.get('sheet'),
        from_row=updated_data.get('from_row'),
        to_row=updated_data.get('to_row'),
        field_id=updated_data.get('field_id'),
    )

    assert updated_instance.data_url == update_result.data_url
    assert updated_instance.sheet == update_result.sheet
    assert updated_instance.from_row == update_result.from_row
    assert updated_instance.to_row == update_result.to_row
    assert updated_instance.field_id == update_result.field_id


@mock.patch('app.services.SettingAutocompleteService.get_by_id')
def test_update_not_exist_field(service_mock, setting_autocomplete_data_with_id):
    service_mock.return_value = None
    update_result = SettingAutocompleteService.update(
        setting_autocomplete_id=setting_autocomplete_data_with_id.get('id'))

    assert update_result is None


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.SettingAutocompleteService.get_by_id')
def test_delete(mock_get, mock_delete, setting_autocomplete_data_with_id):
    instance = SettingAutocomplete(**setting_autocomplete_data_with_id)
    mock_get.return_value = instance
    mock_delete.return_value = None

    result = SettingAutocompleteService.delete(setting_autocomplete_data_with_id.get('id'))

    assert result == True


@mock.patch('app.DB.session.delete')
@mock.patch('app.services.SettingAutocompleteService.get_by_id')
def test_delete_by_group_and_user_id_error(mock_get, mock_delete,
                                           setting_autocomplete_data_with_id):
    mock_get.return_value = None
    mock_delete.return_value = None

    result = SettingAutocompleteService.delete(setting_autocomplete_data_with_id.get('id'))

    assert result == None


@mock.patch('app.models.SettingAutocomplete.query')
def test_get_by_id(query, setting_autocomplete_data):
    instance = SettingAutocomplete(**setting_autocomplete_data)
    query.get.return_value = instance
    test_instance = SettingAutocompleteService.get_by_id(1)

    assert instance.data_url == test_instance.data_url
    assert instance.sheet == test_instance.sheet
    assert instance.from_row == test_instance.from_row
    assert instance.to_row == test_instance.to_row
    assert instance.field_id == test_instance.field_id


@mock.patch('app.models.SettingAutocomplete.query')
def test_get_by_field_id(query, setting_autocomplete_data):
    instance = SettingAutocomplete(**setting_autocomplete_data)
    query.filter_by.return_value.first.return_value = instance
    test_instance = SettingAutocompleteService.get_by_field_id(1)

    assert instance.data_url == test_instance.data_url
    assert instance.sheet == test_instance.sheet
    assert instance.from_row == test_instance.from_row
    assert instance.to_row == test_instance.to_row
    assert instance.field_id == test_instance.field_id


@mock.patch('app.models.SettingAutocomplete.query')
def test_filter(query, setting_autocomplete_data_with_id):
    instance = SettingAutocomplete(**setting_autocomplete_data_with_id)

    query.filter_by.return_value.all.return_value = [instance]
    test_list = SettingAutocompleteService.filter(
        setting_autocomplete_id=setting_autocomplete_data_with_id.get('id'),
        data_url=setting_autocomplete_data_with_id.get('data_url'),
        sheet=setting_autocomplete_data_with_id.get('sheet'),
        from_row=setting_autocomplete_data_with_id.get('from_row'),
        to_row=setting_autocomplete_data_with_id.get('to_row'),
        field_id=setting_autocomplete_data_with_id.get('field_id')
    )

    test_instance = test_list[0]

    assert instance.data_url == test_instance.data_url
    assert instance.sheet == test_instance.sheet
    assert instance.from_row == test_instance.from_row
    assert instance.to_row == test_instance.to_row
    assert instance.field_id == test_instance.field_id
