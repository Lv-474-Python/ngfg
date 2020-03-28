"""
Test SheetManager
"""

import mock
import pytest

from app.models import Field, Range, FieldRange, ChoiceOption, SettingAutocomplete
from app.services import FieldService
from app.helper.errors import FieldNotExist, SettingAutocompleteNotExist

from services_test_data import (
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
    name, owner_id, field_type = test_input
    mock_field_create.return_value = None

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
    name, owner_id, field_type = test_input
    mock_field_create.return_value = None

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
def check_for_range(data, expected):
    """
    Test FieldService get_additional_options()
    Test case when method executed successfully
    """
    result = FieldService.check_for_range(data)

    assert result == expected
