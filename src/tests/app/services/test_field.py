import pytest
import mock

from app.services import FieldService
from app.models import Field, SettingAutocomplete, Range, FieldRange, ChoiceOption


@pytest.fixture()
def field_data():
    data = {
        'id': 1,
        'name': 'TestName',
        'field_type': 1,
        'owner_id': 1,
        'is_strict': True
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


# @mock.patch('app.services.FieldService.update')
# @mock.patch('app.services.FieldService.delete')
# @mock.patch('app.services.FieldRangeService.get_by_field_id')
# def test_update_text_or_number_field_delete_range_not_deleted(
#         field_range_service_mock,
#         field_service_mock_delete,
#         field_service_mock_update,
#         text_or_number_update_data,
#         range_data
# ):
#     """
#     Test update_text_or_number delete range, when range not deleted from database
#     Raise FieldRangeNotDeleted()
#     """
#     field_service_mock_update.return_value = text_or_number_update_data
#     field_service_mock_delete.return_value = None
#     delete_range = True
#     field_range_service_mock.return_value = range_data
#
#     updated = FieldService.update_text_or_number_field(  # pylint: disable=too-many-arguments
#         field_id=text_or_number_update_data.get('id'),
#         name=text_or_number_update_data.get('name'),
#         range_min=text_or_number_update_data.get('range_min'),
#         range_max=text_or_number_update_data.get('range_max'),
#         delete_range=delete_range,
#         is_strict=text_or_number_update_data.get('is_strict'))
#
#     assert updated is None
#
#
# @mock.patch('app.schemas.FieldNumberTextSchema')
# @mock.patch('app.services.RangeService')
# @mock.patch('app.services.FieldRangeService')
# @mock.patch('app.services.FieldService.update')
# def test_update_text_or_number_field_update_range(
#         field_service_mock,
#         field_range_service_mock,
#         range_service_mock,
#         schema_mock,
#         text_or_number_update_data,
#         field_data,
#         range_data
# ):
#     """
#     Test update_text_or_number, update range
#     """
#     field_service_mock.return_value = Field(**field_data)
#     schema_mock.dump.return_value = field_data
#
#     field_range_service_mock.get_by_field_id.return_value = range_data
#     range_service_mock.create.return_value = None
#     field_range_service_mock.update.return_value = None
#
#     delete_range = False
#     updated = FieldService.update_text_or_number_field(  # pylint: disable=too-many-arguments
#         field_id=text_or_number_update_data.get('id'),
#         name=text_or_number_update_data.get('name'),
#         range_min=text_or_number_update_data.get('range_min'),
#         range_max=text_or_number_update_data.get('range_max'),
#         delete_range=delete_range,
#         is_strict=text_or_number_update_data.get('is_strict'))
#
#     assert text_or_number_update_data['name'] == updated['name']
#     assert text_or_number_update_data['id'] == updated['id']
#     assert text_or_number_update_data['range_min'] == updated['range']['min']
#     assert text_or_number_update_data['range_max'] == updated['range']['max']
#
#
# @mock.patch('app.services.FieldService.get_additional_options')
# @mock.patch('app.services.FieldRangeService.create')
# @mock.patch('app.services.RangeService.create')
# @mock.patch('app.services.FieldRangeService.get_by_field_id')
# @mock.patch('app.services.FieldService.update')
# @mock.patch('app.schemas.FieldNumberTextSchema.dump')
# def test_update_text_or_number_create_range(
#         schema_mock,
#         field_service_update,
#         field_range_get,
#         range_create,
#         field_range_create,
#         get_add_options,
#         field_data,
#         range_data,
#         field_range_data
# ):
#     """
#     Test text or number update, create range
#     """
#     field = Field(**field_data)
#     f_range = Range(**range_data)
#     field_range = FieldRange(**field_range_data)
#
#     field_service_update.return_value = field
#     schema_mock.return_value = field_data
#     field_range_get.return_value = None
#     range_create.return_value = f_range
#     field_range_create.return_value = field_range
#     get_add_options.return_value = {'range': range_data}
#
#     delete_range = False
#
#     updated = FieldService.update_text_or_number_field(
#             field_id=field.id,
#             name=field.name,
#             range_max=f_range.max,
#             range_min=f_range.min,
#             delete_range=delete_range,
#             is_strict=field.is_strict
#     )
#     print(updated)
#     assert updated['name'] == field.name
#     assert updated['range']['min'] == f_range.min
#     assert updated['range']['max'] == f_range.max


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

    assert result == False
