"""
FieldService tests
"""

import mock
import pytest

from app.models import Field, Range, FieldRange, ChoiceOption, SettingAutocomplete
from app.services import FieldService
from app.helper.errors import FieldNotExist, SettingAutocompleteNotExist

from .services_test_data import (
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITHOUT_RANGE_DATA,
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITH_RANGE_DATA,
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_ERROR_DATA,
    FIELD_SERVICE_CREATE_TEXT_AREA_TRUE_DATA,
    FIELD_SERVICE_CREATE_TEXT_AREA_ERROR_DATA,
    FIELD_SERVICE_CREATE_RADIO_FIELD_TRUE_DATA,
    FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_OPTIONS_DATA,
    FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_FIELD_DATA,
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITHOUT_RANGE_DATA,
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITH_RANGE_DATA,
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_ERROR_DATA,
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_TRUE_DATA,
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_FIELD_DATA,
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_SETTINGS_DATA,
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_TRUE_DATA,
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_EMPTY_DATA,
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_TRUE_DATA,
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_ERROR_DATA,
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_TRUE_DATA,
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_ERROR_DATA,
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_NUMBER_TEXT_DATA,
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_TEXT_AREA_DATA,
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_RADIO_CHECKBOX_DATA,
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_AUTOCOMPLETE_DATA,
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA,
    FIELD_SERVICE_CHECK_FOR_RANGE_DATA
)


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


@pytest.fixture()
def autocomplete_field_data():
    data = {
        'id': 1,
        'field_id': 1,
        'data_url': 'https://docs.google.com/spreadsheets/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit#gid=0',
        'sheet': 'sheet',
        'from_row': 'A1',
        'to_row': 'A100'
    }
    return data


@pytest.fixture()
def text_or_number_update_data():
    data = {
        'id': 1,
        'name': 'TestName',
        'range_min': 0,
        'range_max': 100,
        'is_strict': True
    }
    return data


@pytest.fixture()
def range_data():
    data = {
        'id': 1,
        'min': 0,
        'max': 100,
    }
    return data


@pytest.fixture()
def field_range_data():
    data = {
        'id': 1,
        'field_id': 1,
        'range_id': 1,
    }
    return data


@pytest.fixture()
def choice_option_data():
    data = {
        'id': 1,
        'field_id': 1,
        'option_text': 'optionText',
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


# create_text_or_number_field
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITHOUT_RANGE_DATA
)
@mock.patch('app.services.FieldService.create')
def test_create_text_or_number_field_without_range(
        mock_field_create,
        test_input):
    """
    Test FieldService create_text_or_number_field()
    Test case when method text or number field is created without range
    """
    name, owner_id, field_type, is_strict = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
        is_strict=is_strict
    )
    mock_field_create.return_value = field

    result = FieldService.create_text_or_number_field(
        name,
        owner_id,
        field_type,
        is_strict
    )

    assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] ==field.owner_id
    assert result['fieldType'] == field.field_type
    assert result['isStrict'] == field.is_strict
    # assert result['created'] == field.created


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITH_RANGE_DATA
)
@mock.patch('app.services.field_range.FieldRangeService.create')
@mock.patch('app.services.range.RangeService.create')
@mock.patch('app.services.field.FieldService.create')
def test_create_text_or_number_field_with_range(
        mock_field_create,
        mock_range_create,
        mock_field_range_create,
        test_input):
    """
    Test FieldService create_text_or_number_field()
    Test case when method text or number field is created with range
    """
    name, owner_id, field_type, is_strict, range_min, range_max = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
        is_strict=is_strict
    )
    range_ = Range(
        min=range_min,
        max=range_max
    )

    mock_field_create.return_value = field
    mock_range_create.return_value = range_
    mock_field_range_create.return_value = None

    result = FieldService.create_text_or_number_field(
        name,
        owner_id,
        field_type,
        is_strict,
        range_min,
        range_max
    )

    assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    assert result['isStrict'] == field.is_strict
    # assert result['created'] == field.created
    assert result['range']['min'] == range_min
    assert result['range']['max'] == range_max


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_ERROR_DATA
)
@mock.patch('app.services.field.FieldService.create')
def test_create_text_or_number_field_error(mock_field_create, test_input):
    """
    Test FieldService create_text_or_number_field()
    Test case when method raised FieldAlreadyExist and returned None
    """
    mock_field_create.return_value = None

    name, owner_id, field_type = test_input
    result = FieldService.create_text_or_number_field(name, owner_id, field_type)

    assert result is None


# create_text_area
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_TEXT_AREA_TRUE_DATA
)
@mock.patch('app.services.FieldService.create')
def test_create_text_area_true(mock_field_create, test_input):
    """
    Test FieldService create_text_area()
    Test case when method executed successfully
    """
    name, owner_id, field_type = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    mock_field_create.return_value = field

    result = FieldService.create_text_area(name, owner_id, field_type)

    assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    assert result['created'] == field.created


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_TEXT_AREA_ERROR_DATA
)
@mock.patch('app.services.field.FieldService.create')
def test_create_text_area_error(mock_field_create, test_input):
    """
    Test FieldService create_text_area()
    Test case when method raised FieldAlreadyExist and returned None
    """
    mock_field_create.return_value = None

    name, owner_id, field_type = test_input
    result = FieldService.create_text_area(name, owner_id, field_type)

    assert result is None


# create_radio_field
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_RADIO_FIELD_TRUE_DATA
)
@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldService.create')
def test_create_radio_field_true(
        mock_field_create,
        mock_choice_option_create,
        test_input):
    """
    Test FieldService create_radio_field()
    Test case when method executed successfully
    """
    name, owner_id, field_type, choice_options, is_strict = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    mock_field_create.return_value = field
    mock_choice_option_create.return_value = None

    result = FieldService.create_radio_field(
        name,
        owner_id,
        field_type,
        choice_options,
        is_strict
    )

    # assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    # assert result['created'] == field.created
    assert result['choiceOptions'] == choice_options


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_OPTIONS_DATA
)
def test_create_radio_field_not_options(test_input):
    """
    Test FieldService create_radio_field()
    Test case when choice_options weren't passed
    Method raised ChoiceNotSend and returned None
    """
    name, owner_id, field_type, choice_options = test_input
    result = FieldService.create_radio_field(name, owner_id, field_type, choice_options)

    assert result is None


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_FIELD_DATA
)
@mock.patch('app.services.field.FieldService.create')
def test_create_radio_field_not_field(mock_field_create, test_input):
    """
    Test FieldService create_radio_field()
    Test case when field wasn't created
    Method raised FieldAlreadyExist and returned None
    """
    name, owner_id, field_type, choice_options = test_input
    mock_field_create.return_value = None

    result = FieldService.create_radio_field(
        name,
        owner_id,
        field_type,
        choice_options
    )

    assert result is None


# create_checkbox_field
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITHOUT_RANGE_DATA
)
@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldService.create')
def test_create_checkbox_field_without_range(
        mock_field_create,
        mock_choice_option_create,
        test_input):
    """
    Test FieldService create_checkbox_field()
    Test case when method checkbox field is created without range
    """
    name, owner_id, field_type, choice_options, is_strict = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    mock_field_create.return_value = field
    mock_choice_option_create.return_value = None

    result = FieldService.create_checkbox_field(
        name,
        owner_id,
        field_type,
        choice_options,
        is_strict
    )

    # assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    # assert result['created'] == field.created
    assert result['choiceOptions'] == choice_options


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITH_RANGE_DATA
)
@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldRangeService.create')
@mock.patch('app.services.RangeService.create')
@mock.patch('app.services.FieldService.create')
def test_create_checkbox_field_with_range(
        mock_field_create,
        mock_range_create,
        mock_field_range_create,
        mock_choice_option_create,
        test_input):
    """
    Test FieldService create_checkbox_field()
    Test case when method checkbox field is created with range
    """
    name, owner_id, field_type, choice_options, is_strict, range_min, range_max = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    range_ = Range(
        min=range_min,
        max=range_max
    )

    mock_field_create.return_value = field
    mock_range_create.return_value = range_
    mock_field_range_create.return_value = None
    mock_choice_option_create.return_value = None

    result = FieldService.create_checkbox_field(
        name,
        owner_id,
        field_type,
        choice_options,
        is_strict,
        range_min,
        range_max
    )

    # assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    # assert result['created'] == field.created
    assert result['choiceOptions'] == choice_options
    assert result['range']['min'] == range_min
    assert result['range']['max'] == range_max


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_ERROR_DATA
)
def test_create_checkbox_field_error(test_input):
    """
    Test FieldService create_checkbox_field()
    Test case when method raised ChoiceNotSend and return None
    """
    name, owner_id, field_type, choice_options = test_input
    result = FieldService.create_checkbox_field(name, owner_id, field_type, choice_options)

    assert result is None


# create_autocomplete_field
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_TRUE_DATA
)
@mock.patch('app.services.SettingAutocompleteService.create')
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_true(
        mock_field_create,
        mock_settings_create,
        test_input):
    """
    Test FieldService create_autocomplete_field()
    Test case when method executed successfully
    """
    name, owner_id, field_type, data_url, sheet, from_row, to_row = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    settings = SettingAutocomplete(
        data_url=data_url,
        sheet=sheet,
        from_row=from_row,
        to_row=to_row,
        field_id=field.id
    )

    mock_field_create.return_value = field
    mock_settings_create.return_value = settings

    result = FieldService.create_autocomplete_field(
        name,
        owner_id,
        field_type,
        data_url,
        sheet,
        from_row,
        to_row
    )

    # assert result['id'] == field.id
    assert result['name'] == field.name
    assert result['ownerId'] == field.owner_id
    assert result['fieldType'] == field.field_type
    # assert result['created'] == field.created
    assert result['settingAutocomplete']['dataUrl'] == settings.data_url
    assert result['settingAutocomplete']['sheet'] == settings.sheet
    assert result['settingAutocomplete']['fromRow'] == settings.from_row
    assert result['settingAutocomplete']['toRow'] == settings.to_row

    # якщо тут вивести field, result, settings (то settings не виведе бо в неї field None і ми типу з None беремо id в __repr__)


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_FIELD_DATA
)
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_not_field(mock_field_create, test_input):
    """
    Test FieldService create_autocomplete_field()
    Test case when field wasn't created
    Method raised FieldNotExist and returned None
    """
    name, owner_id, field_type, data_url, sheet, from_row, to_row = test_input
    mock_field_create.return_value = None

    result = FieldService.create_autocomplete_field(
        name,
        owner_id,
        field_type,
        data_url,
        sheet,
        from_row,
        to_row
    )

    assert result is None

    # там рейситься FieldNotExist а має FieldAlreadyExist або FieldNotCreated
    # швидше всього FieldAlreadyExist бо до того це було


@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_SETTINGS_DATA
)
@mock.patch('app.services.SettingAutocompleteService.create')
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_not_settings(
        mock_field_create,
        mock_settings_create,
        test_input):
    """
    Test FieldService create_autocomplete_field()
    Test case when settings wasn't created
    Method raised SettingAutocompleteNotExist and returned None
    """
    name, owner_id, field_type, data_url, sheet, from_row, to_row = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )

    mock_field_create.return_value = field
    mock_settings_create.return_value = None

    result = FieldService.create_autocomplete_field(
        name,
        owner_id,
        field_type,
        data_url,
        sheet,
        from_row,
        to_row
    )

    assert result is None

    # там рейситься SettingAutocompleteNotExist а має SettingAutocompleteAlreadyExist або SettingAutocompleteNotCreated
    # швидше всього SettingAutocompleteAlreadyExist


# _get_text_or_number_additional_options
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_TRUE_DATA
)
@mock.patch('app.services.RangeService.get_by_id')
@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_get_text_or_number_additional_options_true(
        mock_field_range_get,
        mock_field_get,
        mock_range_get,
        test_input):
    """
    Test FieldService _get_text_or_number_additional_options()
    Test case when settings method executed successfully
    """
    name, owner_id, field_type, is_strict, range_min, range_max = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
        is_strict=is_strict
    )
    range_ = Range(
        min=range_min,
        max=range_max
    )
    field_range = FieldRange(
        field_id=field.id,
        range_id=range_.id
    )

    mock_field_range_get.return_value = field_range
    mock_field_get.return_value = field
    mock_range_get.return_value = range_

    result = FieldService._get_text_or_number_additional_options(field.id)

    assert result['isStrict'] == field.is_strict
    assert result['range']['min'] == range_.min
    assert result['range']['max'] == range_.max


@pytest.mark.parametrize(
    "test_input, expected",
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_EMPTY_DATA
)
@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_get_text_or_number_additional_options_empty(
        mock_field_range_get,
        mock_field_get,
        test_input,
        expected):
    """
    Test FieldService _get_text_or_number_additional_options()
    Test case when method returned empty dict
    """
    name, owner_id, field_type = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )

    mock_field_range_get.return_value = None
    mock_field_get.return_value = field

    result = FieldService._get_text_or_number_additional_options(field.id)

    assert result == expected


# _get_choice_additional_options
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_TRUE_DATA
)
@mock.patch('app.services.RangeService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_get_choice_additional_options_true(
        mock_option_filter,
        mock_field_range_get,
        mock_range_get,
        test_input):
    """
    Test FieldService _get_choice_additional_options()
    Test case when method executed successfully
    """
    field_id, options, range_min, range_max = test_input

    choice_options = [
        ChoiceOption(field_id=field_id, option_text=option) for option in options
    ]
    range_ = Range(
        min=range_min,
        max=range_max
    )
    field_range = FieldRange(
        field_id=field_id,
        range_id=range_.id
    )

    mock_option_filter.return_value = choice_options
    mock_field_range_get.return_value = field_range
    mock_range_get.return_value = range_

    result = FieldService._get_choice_additional_options(field_id)

    assert options == result['choiceOptions']
    assert range_.min == result['range']['min']
    assert range_.max == result['range']['max']


@pytest.mark.parametrize(
    "field_id",
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_get_choice_additional_options_error(
        mock_option_filter,
        mock_field_range_get,
        field_id):
    """
    Test FieldService _get_choice_additional_options()
    Test case when method raised FieldNotExist
    """
    mock_option_filter.return_value = None
    mock_field_range_get.return_value = None

    with pytest.raises(FieldNotExist):
        FieldService._get_choice_additional_options(field_id)


# _get_autocomplete_additional_options
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_TRUE_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.get_data_with_range')
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
def test_get_autocomplete_additional_options_true(
        mock_settings_get,
        mock_manager_get_data,
        test_input):
    """
    Test FieldService _get_choice_additional_options()
    Test case when method executed successfully
    """
    field_id, data_url, sheet, from_row, to_row, sheet_data = test_input

    settings = SettingAutocomplete(
        data_url=data_url,
        sheet=sheet,
        from_row=from_row,
        to_row=to_row,
        field_id=field_id
    )

    mock_settings_get.return_value = settings
    mock_manager_get_data.return_value = sheet_data

    result = FieldService._get_autocomplete_additional_options(field_id)

    assert result['settingAutocomplete']['dataUrl'] == data_url
    assert result['settingAutocomplete']['sheet'] == sheet
    assert result['settingAutocomplete']['fromRow'] == from_row
    assert result['settingAutocomplete']['toRow'] == to_row
    assert result['values'] == sheet_data


@pytest.mark.parametrize(
    "field_id",
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
def test_get_autocomplete_additional_options_error(mock_settings_get, field_id):
    """
    Test FieldService _get_choice_additional_options()
    Test case when method raised SettingAutocompleteNotExist
    """
    mock_settings_get.return_value = None

    with pytest.raises(SettingAutocompleteNotExist):
        FieldService._get_autocomplete_additional_options(field_id)


# get_additional_options
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_NUMBER_TEXT_DATA
)
@mock.patch('app.services.FieldService._get_text_or_number_additional_options')
def test_get_additional_options_number_text(
        mock_field_get_options,
        field_id,
        field_type,expected):
    """
    Test FieldService get_additional_options()
    Test case when field type is number or text
    """
    mock_field_get_options.return_value = expected

    result = FieldService.get_additional_options(field_id, field_type)

    assert result == expected


@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_TEXT_AREA_DATA
)
def test_get_additional_options_text_area(field_id, field_type, expected):
    """
    Test FieldService get_additional_options()
    Test case when field type is textarea
    """
    result = FieldService.get_additional_options(field_id, field_type)

    assert result == expected


@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_RADIO_CHECKBOX_DATA
)
@mock.patch('app.services.FieldService._get_choice_additional_options')
def test_get_additional_options_radio_checkbox(
        mock_field_get_options,
        field_id,
        field_type,
        expected):
    """
    Test FieldService get_additional_options()
    Test case when field type is radio or checkbox
    """
    mock_field_get_options.return_value = expected

    result = FieldService.get_additional_options(field_id, field_type)

    assert result == expected


@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_AUTOCOMPLETE_DATA
)
@mock.patch('app.services.FieldService._get_autocomplete_additional_options')
def test_get_additional_options_autocomplete(
        mock_field_get_options,
        field_id,
        field_type,
        expected):
    """
    Test FieldService get_additional_options()
    Test case when field type is autocomplete
    """
    mock_field_get_options.return_value = expected

    result = FieldService.get_additional_options(field_id, field_type)

    assert result == expected


@pytest.mark.parametrize(
    "field_id, field_type",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.FieldService._get_choice_additional_options')
def test_get_additional_options_error(
        mock_field_get_options,
        field_id,
        field_type):
    """
    Test FieldService get_additional_options()
    Test case when method raised FieldNotExist and returned None
    """
    mock_field_get_options.side_effect = FieldNotExist()

    result = FieldService.get_additional_options(field_id, field_type)

    assert result is None


# check_for_range
@pytest.mark.parametrize(
    "data, expected",
    FIELD_SERVICE_CHECK_FOR_RANGE_DATA
)
def test_check_for_range(data, expected):
    """
    Test FieldService get_additional_options()
    Test case when method executed successfully
    """
    result = FieldService.check_for_range(data)

    assert result == expected


@mock.patch('app.services.FieldService.update')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_update_text_or_number_field_delete_range_not_exist(
        field_range_service_mock,
        field_service_mock,
        text_or_number_update_data
):
    """
    Test update_text_or_number delete range, when range not found
    Raise FieldRangeNotDeleted()
    """
    field_service_mock.return_value = text_or_number_update_data
    field_range_service_mock.return_value = None
    delete_range = True

    updated = FieldService.update_text_or_number_field(  # pylint: disable=too-many-arguments
        field_id=text_or_number_update_data.get('id'),
        name=text_or_number_update_data.get('name'),
        range_min=text_or_number_update_data.get('range_min'),
        range_max=text_or_number_update_data.get('range_max'),
        delete_range=delete_range,
        is_strict=text_or_number_update_data.get('is_strict'))

    assert updated is None


@mock.patch('app.services.FieldRangeService.delete')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldNumberTextSchema.dump')
def test_update_text_or_number_delete_range_not_deleted(
        schema_mock,
        field_service_update,
        field_range_get,
        field_range_delete,
        field_data,
        field_range_data
):
    """
    Test update_text_or_number delete range, when range not deleted from database
    Raise FieldRangeNotDeleted()
    """
    field = Field(**field_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range

    delete_range = True
    field_range_delete.return_value = None

    updated = FieldService.update_text_or_number_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            is_strict=field.is_strict
    )

    assert updated is None


@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldRangeService.update')
@mock.patch('app.services.RangeService.create')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldNumberTextSchema.dump')
def test_update_text_or_number_update_range(
        schema_mock,
        field_service_update,
        field_range_get,
        range_create,
        field_range_update,
        get_add_options,
        field_data,
        range_data,
        field_range_data
):
    """
    Test text or number update, update range
    """
    field = Field(**field_data)
    f_range = Range(**range_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range
    range_create.return_value = f_range
    field_range_update.return_value = field_range
    get_add_options.return_value = {'range': range_data}

    delete_range = False

    updated = FieldService.update_text_or_number_field(
            field_id=field.id,
            name=field.name,
            range_max=f_range.max,
            range_min=f_range.min,
            delete_range=delete_range,
            is_strict=field.is_strict
    )

    assert updated['name'] == field.name
    assert updated['range']['min'] == f_range.min
    assert updated['range']['max'] == f_range.max


@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldRangeService.create')
@mock.patch('app.services.RangeService.create')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldNumberTextSchema.dump')
def test_update_text_or_number_create_range(
        schema_mock,
        field_service_update,
        field_range_get,
        range_create,
        field_range_create,
        get_add_options,
        field_data,
        range_data,
        field_range_data
):
    """
    Test text or number update, create range
    """
    field = Field(**field_data)
    f_range = Range(**range_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = None
    range_create.return_value = f_range
    field_range_create.return_value = field_range
    get_add_options.return_value = {'range': range_data}

    delete_range = False

    updated = FieldService.update_text_or_number_field(
            field_id=field.id,
            name=field.name,
            range_max=f_range.max,
            range_min=f_range.min,
            delete_range=delete_range,
            is_strict=field.is_strict
    )

    assert updated['name'] == field.name
    assert updated['range']['min'] == f_range.min
    assert updated['range']['max'] == f_range.max


@mock.patch('app.schemas.FieldSettingAutocompleteSchema.dump')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
def test_update_autocomplete_field_settings_not_found(
        autocomplete_service_mock,
        field_service_mock,
        schema_mock,
        autocomplete_field_data,
        field_data

):
    """
    Test autocomplete
    Raise SettingAutocompleteNotExist()
    """
    schema_mock.return_value = None
    autocomplete_service_mock.return_value = None
    field_service_mock.return_value = Field(**field_data)

    updated = FieldService.update_autocomplete_field(  # pylint: disable=too-many-arguments
        field_id=autocomplete_field_data.get('id'),
        name=autocomplete_field_data.get('name'),
        data_url=autocomplete_field_data.get('data_url'),
        sheet=autocomplete_field_data.get('sheet'),
        from_row=autocomplete_field_data.get('from_row'),
        to_row=autocomplete_field_data.get('to_row'),
    )

    assert updated is None


@mock.patch('app.schemas.FieldSettingAutocompleteSchema.dump')
@mock.patch('app.services.SettingAutocompleteService.update')
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldService.update')
def test_update_autocomplete_field_success(
        field_service_mock_update,
        field_service_mock_get_additional_options,
        autocomplete_service_mock_get,
        autocomplete_service_mock_upd,
        schema_mock,
        autocomplete_field_data,
        field_data
):
    """
    Test autocomplete successful update
    """
    field = Field(**field_data)
    settings = SettingAutocomplete(**autocomplete_field_data)

    schema_mock.return_value = autocomplete_field_data
    autocomplete_service_mock_get.return_value = settings
    autocomplete_service_mock_upd.return_value = None
    field_service_mock_update.return_value = field
    field_service_mock_get_additional_options.return_value = autocomplete_field_data

    updated = FieldService.update_autocomplete_field(  # pylint: disable=too-many-arguments
        field_id=field.id,
        name=field.name,
        data_url=autocomplete_field_data.get('data_url'),
        sheet=autocomplete_field_data.get('sheet'),
        from_row=autocomplete_field_data.get('from_row'),
        to_row=autocomplete_field_data.get('to_row'),
    )
    assert updated['data_url'] == autocomplete_field_data['data_url']
    assert updated['from_row'] == autocomplete_field_data['from_row']
    assert updated['to_row'] == autocomplete_field_data['to_row']
    assert updated['sheet'] == autocomplete_field_data['sheet']


@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_delete_range_not_exist(
        schema_mock,
        field_service_update,
        field_range_get,
        field_data

):
    """
    Test checkbox update, delete non-existing range
    """
    field = Field(**field_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = None

    delete_range = True

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=None,
    )

    assert updated is None


@mock.patch('app.services.FieldRangeService.delete')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_delete_range_not_deleted(
        schema_mock,
        field_service_update,
        field_range_get,
        field_range_delete,
        field_data,
        range_data

):
    """
    Test checkbox update, range not deleted
    """
    field = Field(**field_data)
    f_range = Range(**range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = f_range
    field_range_delete.return_value = None

    delete_range = True

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=None,
    )

    assert updated is None


@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldRangeService.create')
@mock.patch('app.services.RangeService.create')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_create_range(
        schema_mock,
        field_service_update,
        field_range_get,
        range_create,
        field_range_create,
        field_add_options,
        field_data,
        range_data,
        field_range_data
):
    """
    Test checkbox update, create range
    """
    field = Field(**field_data)
    f_range = Range(**range_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = None
    range_create.return_value = f_range
    field_range_create.return_value = field_range
    field_add_options.return_value = {'range': range_data}

    delete_range = False

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=f_range.max,
            range_min=f_range.min,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=None,
    )

    assert updated['name'] == field.name
    assert updated['range']['min'] == f_range.min
    assert updated['range']['max'] == f_range.max


@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.FieldRangeService.update')
@mock.patch('app.services.RangeService.create')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_update_range(
        schema_mock,
        field_service_update,
        field_range_get,
        range_create,
        field_range_update,
        field_add_options,
        field_data,
        range_data,
        field_range_data
):
    """
    Test checkbox update, update range
    """
    field = Field(**field_data)
    f_range = Range(**range_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range
    range_create.return_value = f_range
    field_range_update.return_value = field_range
    field_add_options.return_value = {'range': range_data}

    delete_range = False

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=f_range.max,
            range_min=f_range.min,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=None,
    )

    assert updated['name'] == field.name
    assert updated['range']['min'] == f_range.min
    assert updated['range']['max'] == f_range.max


@mock.patch('app.services.ChoiceOptionService.get_by_field_and_text')
@mock.patch('app.services.FieldRangeService.delete')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_delete_option_not_exist(
        schema_mock,
        field_service_update,
        field_range_get,
        field_range_delete,
        choice_option_get,
        field_data,
        field_range_data
):
    """
    Test checkbox update, remove choice option that does not exist
    """

    field = Field(**field_data)
    field_range = FieldRange(**field_range_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range

    delete_range = True
    field_range_delete.return_value = True

    choice_option_get.return_value = None

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=['optionToRemove'],
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.delete')
@mock.patch('app.services.ChoiceOptionService.get_by_field_and_text')
@mock.patch('app.services.FieldRangeService.delete')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_delete_option_not_deleted(
        schema_mock,
        field_service_update,
        field_range_get,
        field_range_delete,
        choice_option_get,
        choice_option_delete,
        field_data,
        field_range_data,
        choice_option_data
):
    """
    Test checkbox update, choice option not deleted from database
    """

    field = Field(**field_data)
    field_range = FieldRange(**field_range_data)
    choice_option = ChoiceOption(**choice_option_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range

    delete_range = True
    field_range_delete.return_value = True

    choice_option_get.return_value = choice_option
    choice_option_delete.return_value = None

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            added_choice_options=None,
            removed_choice_options=[choice_option.option_text],
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldRangeService.delete')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldCheckboxSchema.dump')
def test_update_checkbox_delete_option_not_added(
        schema_mock,
        field_service_update,
        field_range_get,
        field_range_delete,
        choice_option_create,
        field_data,
        field_range_data,
        choice_option_data
):
    """
    Test checkbox update, choice option not created
    """

    field = Field(**field_data)
    field_range = FieldRange(**field_range_data)
    choice_option = ChoiceOption(**choice_option_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_range_get.return_value = field_range

    delete_range = True
    field_range_delete.return_value = True

    choice_option_create.return_value = None

    updated = FieldService.update_checkbox_field(
            field_id=field.id,
            name=field.name,
            range_max=None,
            range_min=None,
            delete_range=delete_range,
            added_choice_options=[choice_option.option_text],
            removed_choice_options=None,
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldRadioSchema.dump')
def test_update_radio_delete_option_not_added(
        schema_mock,
        field_service_update,
        choice_option_create,
        field_data,
        choice_option_data
):
    """
    Test radio update, choice option not created
    """

    field = Field(**field_data)
    choice_option = ChoiceOption(**choice_option_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data

    choice_option_create.return_value = None

    updated = FieldService.update_radio_field(
            field_id=field.id,
            name=field.name,
            added_choice_options=[choice_option.option_text],
            removed_choice_options=None,
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.delete')
@mock.patch('app.services.ChoiceOptionService.get_by_field_and_text')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldRadioSchema.dump')
def test_update_radio_delete_option_not_deleted(
        schema_mock,
        field_service_update,
        choice_option_get,
        choice_option_delete,
        field_data,
        choice_option_data
):
    """
    Test radio update, choice option not deleted from database
    """

    field = Field(**field_data)
    choice_option = ChoiceOption(**choice_option_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data

    choice_option_get.return_value = choice_option
    choice_option_delete.return_value = None

    updated = FieldService.update_radio_field(
            field_id=field.id,
            name=field.name,
            added_choice_options=None,
            removed_choice_options=[choice_option.option_text],
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.get_by_field_and_text')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldRadioSchema.dump')
def test_update_radio_delete_option_not_exist(
        schema_mock,
        field_service_update,
        choice_option_get,
        field_data,
):
    """
    Test checkbox update, remove choice option that does not exist
    """

    field = Field(**field_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data

    choice_option_get.return_value = None

    updated = FieldService.update_radio_field(
            field_id=field.id,
            name=field.name,
            added_choice_options=None,
            removed_choice_options=['optionToRemove'],
    )

    assert updated is None


@mock.patch('app.services.ChoiceOptionService.delete')
@mock.patch('app.services.FieldService.get_additional_options')
@mock.patch('app.services.ChoiceOptionService.get_by_field_and_text')
@mock.patch('app.services.FieldService.update')
@mock.patch('app.schemas.FieldRadioSchema.dump')
def test_update_radio_delete_option_success(
        schema_mock,
        field_service_update,
        choice_option_get,
        field_get_add_options,
        choice_option_delete,
        field_data,
        choice_option_data
):
    """
    Test checkbox update, remove choice option successfully
    """

    field = Field(**field_data)
    choice_option = ChoiceOption(**choice_option_data)

    field_service_update.return_value = field
    schema_mock.return_value = field_data
    field_get_add_options.return_value = {'choiceOptions': [choice_option_data]}

    choice_option_get.return_value = choice_option
    choice_option_delete.return_value = True

    updated = FieldService.update_radio_field(
            field_id=field.id,
            name=field.name,
            added_choice_options=None,
            removed_choice_options=['optionToRemove'],
    )

    assert updated['name'] == field.name
    assert updated['choiceOptions'] == [choice_option_data]


@mock.patch('app.services.FormFieldService.filter')
def test_check_form_membership(
        form_field_filter
):
    """
    Test membership check, not in form
    """
    form_field_filter.return_value = None
    result = FieldService.check_form_membership(1)

    assert not result
