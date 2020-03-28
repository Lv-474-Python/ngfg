"""
Test SheetManager
"""

import mock
import pytest

from app.models import Field, Range, FieldRange, ChoiceOption, SettingAutocomplete
from app.services import FieldService
from app.helper.errors import FieldNotExist, SettingAutocompleteNotExist


# create_text_or_number_field
FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITHOUT_RANGE_DATA = [
    ("age", 1, 1, False),
    ("towns", 2, 1, True)
]
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


FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_WITH_RANGE_DATA = [
    ("name", 3, 1, False, 2, None),
    ("city", 4, 2, True, 2, 5)
]
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


FIELD_SERVICE_CREATE_TEXT_OR_NUMBER_FIELD_ERROR_DATA = [
    ("school", 5, 2),
    ("university", 6, 2)
]
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
FIELD_SERVICE_CREATE_TEXT_AREA_TRUE_DATA = [
    ("age", 7, 3),
    ("towns", 8, 3)
]
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


FIELD_SERVICE_CREATE_TEXT_AREA_ERROR_DATA = [
    ("first school", 9, 3),
    ("first university", 10, 3)
]
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


#create_radio_field
FIELD_SERVICE_CREATE_RADIO_FIELD_TRUE_DATA = [
    ("age", 11, 4, ["10", "11", "12"], True),
    ("towns", 12, 4, ["Rivne", "Lviv"], False)
]
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


FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_OPTIONS_DATA = [
    ("words", 13, 4, []),
    ("text", 14, 4, None)
]
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


FIELD_SERVICE_CREATE_RADIO_FIELD_NOT_FIELD_DATA = [
    ("colors", 15, 4, ["r", "g", "b"]),
    ("cmyk", 16, 4, ["c", "m", "y", "k"])
]
@pytest.mark.parametrize(
    "test_input, expected",
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



#create_checkbox_field
FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITHOUT_RANGE_DATA = [
    ("age", 17, 6, ["10", "11", "12"], True),
    ("cities", 18, 6, ["Kyiv", "Lviv"], False)
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITHOUT_RANGE_DATA
)
@mock.patch('app.services.ChoiceOptionService.create')
@mock.patch('app.services.FieldService.create')
def test_create_checkbox_field_without_range(mock_field_create, mock_choice_option_create, test_input):
    """
    """
    name, owner_id, field_type, choice_options, is_strict = test_input
    field = Field(
        name=name,
        owner_id=owner_id,
        field_type=field_type,
    )
    mock_field_create.return_value = field
    mock_choice_option_create.return_value = None

    result = FieldService.create_checkbox_field(name, owner_id, field_type, choice_options, is_strict)

    # assert field.id == result['id']
    assert field.name == result['name']
    assert field.owner_id == result['ownerId']
    assert field.field_type == result['fieldType']
    # assert field.created == result['created']
    assert choice_options == result['choiceOptions']


FIELD_SERVICE_CREATE_CHECKBOX_FIELD_WITH_RANGE_DATA = [
    ("age", 19, 6, ["10", "11", "12"], True, 1, 2),
    ("clowns", 20, 6, ["Kyiv", "Lviv"], False, 1, None)
]
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

    # import pdb ; pdb.set_trace()

    # assert field.id == result['id']
    assert field.name == result['name']
    assert field.owner_id == result['ownerId']
    assert field.field_type == result['fieldType']
    # assert field.created == result['created']
    assert choice_options == result['choiceOptions']
    assert range_min == result['range']['min']
    assert range_max == result['range']['max']


FIELD_SERVICE_CREATE_CHECKBOX_FIELD_ERROR_DATA = [
    (("beasts", 21, 5, []), None),
    (("elks", 22, 5, []), None)
]
@pytest.mark.parametrize(
    "test_input, expected",
    FIELD_SERVICE_CREATE_CHECKBOX_FIELD_ERROR_DATA
)
def test_create_checkbox_field_error(test_input, expected):
    """
    """
    name, owner_id, field_type, choice_options = test_input
    assert FieldService.create_checkbox_field(name, owner_id, field_type, choice_options) == expected



#create_autocomplete_field
FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_TRUE_DATA = [
    ("age", 23, 5, "data_url 1", "sheet 1", "A1", "A11"),
    ("towns", 24, 5, "data_url 2", "sheet 2", "B12", "B15"),
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_TRUE_DATA
)
@mock.patch('app.services.SettingAutocompleteService.create')
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_true(mock_field_create, mock_settings_create, test_input):
    """
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

    # assert field.id == result['id']
    assert field.name == result['name']
    assert field.owner_id == result['ownerId']
    assert field.field_type == result['fieldType']
    # assert field.created == result['created']
    assert settings.data_url == result['settingAutocomplete']['dataUrl']
    assert settings.sheet == result['settingAutocomplete']['sheet']
    assert settings.from_row == result['settingAutocomplete']['fromRow']
    assert settings.to_row == result['settingAutocomplete']['toRow']

    # якщо тут вивести field, result, settings (то settings не виведе бо в неї field None і ми типу з None беремо id)


FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_FIELD_DATA = [
    (("crowns", 25, 5, "data_url 3", "sheet 3", "C1", "C11"), None),
    (("towns", 26, 5, "data_url 4", "sheet 4", "D12", "D15"), None)
]
@pytest.mark.parametrize(
    "test_input, expected",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_FIELD_DATA
)
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_not_field(mock_field_create, test_input, expected):
    """
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

    assert result == expected


FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_SETTINGS_DATA = [
    (("clowns", 27, 5, "data_url 5", "sheet 5", "K1", "K11"), None),
    (("towns", 28, 5, "data_url 6", "sheet 6", "F12", "F15"), None)
]
@pytest.mark.parametrize(
    "test_input, expected",
    FIELD_SERVICE_CREATE_AUTOCOMPLETE_FIELD_NOT_SETTINGS_DATA
)
@mock.patch('app.services.SettingAutocompleteService.create')
@mock.patch('app.services.FieldService.create')
def test_create_autocomplete_field_not_settings(mock_field_create, mock_settings_create, test_input, expected):
    """
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

    assert result == expected



# _get_text_or_number_additional_options
FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_WITH_STRICT_DATA = [
    ("age", 29, 1, True, 1, 2),
    ("name", 30, 1, True, 1, None)
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_WITH_STRICT_DATA
)
@mock.patch('app.services.RangeService.get_by_id')
@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_get_text_or_number_additional_options_with_strict(mock_field_range_get, mock_field_get, mock_range_get, test_input):
    """
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

    assert field.is_strict == result['isStrict']
    assert range_.min == result['range']['min']
    assert range_.max == result['range']['max']


FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_WITHOUT_STRICT_DATA = [
    ("surname", 31, 2, False, 1, 2),
    ("last name", 32, 2, False, 1, None)
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_WITHOUT_STRICT_DATA
)
@mock.patch('app.services.RangeService.get_by_id')
@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_get_text_or_number_additional_options_without_strict(mock_field_range_get, mock_field_get, mock_range_get, test_input):
    """
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

    assert range_.min == result['range']['min']
    assert range_.max == result['range']['max']


FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_EMPTY_DATA = [
    (("surname", 31, 2), {}),
    (("last name", 32, 2), {})
]
@pytest.mark.parametrize(
    "test_input, expected",
    FIELD_SERVICE_GET_TEXT_OR_NUMBER_ADDITIONAL_OPTIONS_EMPTY_DATA
)
@mock.patch('app.services.FieldService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
def test_get_text_or_number_additional_options_empty(mock_field_range_get, mock_field_get, test_input, expected):
    """
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
FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_TRUE_DATA = [
    (1, ["1", "2", "3"], 2, 3),
    (1, ["4", "4", "5"], 2, None)
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_TRUE_DATA
)
@mock.patch('app.services.RangeService.get_by_id')
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_get_choice_additional_options_true(mock_option_filter, mock_field_range_get, mock_range_get, test_input):
    """
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


FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_ERROR_DATA = [
    1,
    2
]
@pytest.mark.parametrize(
    "field_id",
    FIELD_SERVICE_GET_CHOICE_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.FieldRangeService.get_by_field_id')
@mock.patch('app.services.ChoiceOptionService.filter')
def test_get_choice_additional_options_error(mock_option_filter, mock_field_range_get, field_id):
    """
    """
    mock_option_filter.return_value = None
    mock_field_range_get.return_value = None

    with pytest.raises(FieldNotExist):
        FieldService._get_choice_additional_options(field_id)



# _get_autocomplete_additional_options
FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_TRUE_DATA = [
    (1, "http://docs.google.com/spreadsheet/d/asda", "sheet 1", "A1", "A2", ["1.1", "1.2"]),
    (2, "http://docs.google.com/spreadsheet/d/wsrs", "sheet 2", "B1", "B2", ["2.1", "2.2"])
]
@pytest.mark.parametrize(
    "test_input",
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_TRUE_DATA
)
@mock.patch('app.helper.sheet_manager.SheetManager.get_data_with_range')
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
def test_get_autocomplete_additional_options_true(mock_settings_get, mock_manager_get_data, test_input):
    """
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

    assert data_url == result['settingAutocomplete']['dataUrl']
    assert sheet == result['settingAutocomplete']['sheet']
    assert from_row == result['settingAutocomplete']['fromRow']
    assert to_row == result['settingAutocomplete']['toRow']
    assert sheet_data == result['values']


FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_ERROR_DATA = [
    1,
    2
]
@pytest.mark.parametrize(
    "field_id",
    FIELD_SERVICE_GET_AUTOCOMPLETE_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.SettingAutocompleteService.get_by_field_id')
def test_get_autocomplete_additional_options_error(mock_settings_get, field_id):
    """
    """
    mock_settings_get.return_value = None

    with pytest.raises(SettingAutocompleteNotExist):
        FieldService._get_autocomplete_additional_options(field_id)



# get_additional_options
FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_NUMBER_TEXT_DATA = [
    (1, 1, {'isStrict': True, 'range': {'min': 5, 'max': 10}}),
    (1, 2, {'isStrict': False, 'range': {'min': 1, 'max': 10}}),
]
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_NUMBER_TEXT_DATA
)
@mock.patch('app.services.FieldService._get_text_or_number_additional_options')
def test_get_additional_options_number_text(mock_field_get_options, field_id, field_type, expected):
    """
    """
    mock_field_get_options.return_value = expected

    assert FieldService.get_additional_options(field_id, field_type) == expected


FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_TEXT_AREA_DATA = [
    (4, 3, {}),
    (5, 3, {}),
]
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_TEXT_AREA_DATA
)
def test_get_additional_options_text_area(field_id, field_type, expected):
    """
    """
    assert FieldService.get_additional_options(field_id, field_type) == expected


FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_RADIO_CHECKBOX_DATA = [
    (6, 4, {'choiceOptions': ['Yes', 'No']}),
    (7, 6, {'choiceOptions': ['Male', 'Female', 'Other'], 'range': {'min': 1, 'max': 2}}),
]
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_RADIO_CHECKBOX_DATA
)
@mock.patch('app.services.FieldService._get_choice_additional_options')
def test_get_additional_options_radio_checkbox(mock_field_get_options, field_id, field_type, expected):
    """
    """
    mock_field_get_options.return_value = expected

    assert FieldService.get_additional_options(field_id, field_type) == expected


FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_AUTOCOMPLETE_DATA = [
    (8, 5, {
        'settingAutocomplete': {
            'dataUrl': 'http://docs.google.com/spreadsheet/d/a', 
            'sheet': 'sheet',
            'fromRow': 'A1',
            'toRow': 'A2'
        },
        'values': ['male', 'female']
    }),
    (9, 5, {
        'settingAutocomplete': {
            'dataUrl': 'http://docs.google.com/spreadsheet/d/aasd', 
            'sheet': 'sheet 2',
            'fromRow': 'B1',
            'toRow': 'C2'
        },
        'values': ['yes', 'no']
    } ),
]
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_AUTOCOMPLETE_DATA
)
@mock.patch('app.services.FieldService._get_autocomplete_additional_options')
def test_get_additional_options_autocomplete(mock_field_get_options, field_id, field_type, expected):
    """
    """
    mock_field_get_options.return_value = expected

    assert FieldService.get_additional_options(field_id, field_type) == expected


FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA = [
    (9, 4, None),
    (10, 6, None),
]
@pytest.mark.parametrize(
    "field_id, field_type, expected",
    FIELD_SERVICE_GET_ADDITIONAL_OPTIONS_ERROR_DATA
)
@mock.patch('app.services.FieldService._get_choice_additional_options')
def test_get_additional_options_error(mock_field_get_options, field_id, field_type, expected):
    """
    """
    mock_field_get_options.side_effect = FieldNotExist()

    assert FieldService.get_additional_options(field_id, field_type) == expected


# check_for_range
FIELD_SERVICE_CHECK_FOR_RANGE_DATA = [
    ({'range': {'min': 2, 'max': 4}}, (2, 4)),
    ({}, (None, None))
]
@pytest.mark.parametrize(
    "data, expected",
    FIELD_SERVICE_CHECK_FOR_RANGE_DATA
)
def test_check_for_range(data, expected):
    """
    """
    assert FieldService.check_for_range(data) == expected
