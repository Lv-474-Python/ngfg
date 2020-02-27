"""
Field Service
"""
from app import DB, LOGGER
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType
from app.helper.errors import (
    FieldNotExist,
    ChoiceNotSend,
    SettingAutocompleteNotExist,
    FieldAlreadyExist
)
from app.models import (
    Field,
    FieldSchema,
    FieldNumberTextSchema,
    FieldSettingAutocompleteSchema,
    FieldRadioSchema,
    FieldCheckboxSchema,
    FieldPutSchema,
    BasicField
)
from app.services.choice_option import ChoiceOptionService
from app.services.field_range import FieldRangeService
from app.services.range import RangeService
from app.services.setting_autocomplete import SettingAutocompleteService
from app.services.form_field import FormFieldService


#pylint: disable=too-many-public-methods
class FieldService:
    """
    Field Service class
    """

    @staticmethod
    @transaction_decorator
    def create(name, owner_id, field_type, is_strict=False):
        """
        Field model create method

        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :param is_strict: if field is strict
        :return: created field instance
        """
        instance = Field(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
            is_strict=is_strict
        )
        DB.session.add(instance)
        return instance

    @staticmethod
    def get_by_id(field_id):
        """
        Field model get by id method

        :param field_id: field id
        :return: Field instance or None
        """
        instance = Field.query.get(field_id)
        return instance

    @staticmethod
    def filter(
            field_id=None,
            name=None,
            owner_id=None,
            field_type=None,
            is_strict=None):
        """
        Field model filter method

        :param field_id: field id
        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :param is_strict: if field is strict
        :return: list of fields
        """
        filter_data = {}
        if field_id is not None:
            filter_data['id'] = field_id
        if name is not None:
            filter_data['name'] = name
        if owner_id is not None:
            filter_data['owner_id'] = owner_id
        if field_type is not None:
            filter_data['field_type'] = field_type
        if is_strict is not None:
            filter_data['is_strict'] = is_strict

        result = Field.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def update(
            field_id,
            name=None,
            owner_id=None,
            field_type=None,
            is_strict=None):
        """
        Field model update method

        :param field_id: field id
        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :param is_strict: if field is strict
        :return: updated field instance
        """
        instance = FieldService.get_by_id(field_id)
        if instance is None:
            raise FieldNotExist()

        if name is not None:
            instance.name = name
        if owner_id is not None:
            instance.owner_id = owner_id
        if field_type is not None:
            instance.field_type = field_type
        if is_strict is not None:
            instance.is_strict = is_strict
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def delete(field_id):
        """
        Field model delete method

        :param field_id: field id
        :return: if field was deleted
        """
        instance = FieldService.get_by_id(field_id)
        if instance is None:
            raise FieldNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = FieldSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def field_to_json(data, many=False):
        """
        Get data in json format

        """
        schema = FieldNumberTextSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def validate(data):
        """
        Global post validation

        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = FieldSchema().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_setting_autocomplete(data):
        """
        Validation for setting autocomplete items

        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = FieldSettingAutocompleteSchema().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_text_or_number(data):
        """
        Validation for text or number field

        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = FieldNumberTextSchema().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_radio(data):
        """
        Validation for setting autocomplete items

        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = FieldRadioSchema().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_checkbox(data):
        """
        Validation for setting autocomplete items
        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = FieldCheckboxSchema().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_textarea(data):
        """
        Validation for text area field
        :param data:
        :return: errors if validation failed else empty dict
        """
        errors = BasicField().validate(data)
        return (not bool(errors), errors)

    @staticmethod
    @transaction_decorator
    def create_text_or_number_field(  # pylint: disable=too-many-arguments
            name,
            owner_id,
            field_type,
            is_strict=False,
            range_min=None,
            range_max=None):
        """
        Creates number or text field with range if needed

        :param name:
        :param owner_id:
        :param field_type:
        :param is_strict:
        :param range_min:
        :param range_max:
        :return:
        """

        field = FieldService.create(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
            is_strict=is_strict
        )
        if field is None:
            raise FieldAlreadyExist()
        data = FieldNumberTextSchema().dump(field)

        if range_min is not None or range_max is not None:
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(
                field_id=field.id,
                range_id=range_instance.id)

            data['range'] = {
                'min': range_min,
                'max': range_max
            }

        return data

    @staticmethod
    @transaction_decorator
    def create_text_area(name, owner_id, field_type):
        """

        :param name:
        :param owner_id:
        :param field_type:
        :return:
        """

        field = FieldService.create(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
        )
        if field is None:
            raise FieldAlreadyExist()
        data = BasicField().dump(field)
        return data

    @staticmethod
    @transaction_decorator
    def create_radio_field(
            name,
            owner_id,
            field_type,
            choice_options,
            is_strict=False):
        """
        Creates radio or check field

        :param name:
        :param owner_id:
        :param field_type:
        :param is_strict:
        :param choice_options:
        :return:
        """

        if not choice_options:
            raise ChoiceNotSend()

        field = FieldService.create(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
            is_strict=is_strict
        )

        data = FieldRadioSchema().dump(field)

        for option in choice_options:
            data['choice_options'].append(option)
            ChoiceOptionService.create(field.id, option)
        return data

    @staticmethod
    @transaction_decorator
    def create_checkbox_field(  # pylint: disable=too-many-arguments
            name,
            owner_id,
            field_type,
            choice_options,
            is_strict=False,
            range_min=None,
            range_max=None):
        """
        Creates check field with optional range

        :param name:
        :param owner_id:
        :param field_type:
        :param is_strict:
        :param choice_options:
        :param range_min:
        :param range_max:
        :return:
        """

        if not choice_options:
            raise ChoiceNotSend()

        field = FieldService.create(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
            is_strict=is_strict
        )
        data = FieldRadioSchema().dump(field)

        if range_min is not None or range_max is not None:
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(field_id=field.id,
                                     range_id=range_instance.id)
            data['range'] = {
                'min': range_min,
                'max': range_max
            }

        for option in choice_options:
            data['choice_options'].append(option)
            ChoiceOptionService.create(field.id, option)
        return data

    @staticmethod
    @transaction_decorator
    def create_autocomplete_field(  # pylint: disable=too-many-arguments
            name,
            owner_id,
            field_type,
            data_url,
            sheet,
            from_row,
            to_row,
            is_strict=False):
        """
        Creates autocomplete field

        :param name:
        :param owner_id:
        :param field_type:
        :param is_strict:
        :param data_url:
        :param sheet:
        :param from_row:
        :param to_row:
        :return:
        """

        field = FieldService.create(
            name=name,
            owner_id=owner_id,
            field_type=field_type,
            is_strict=is_strict
        )

        if field is None:
            raise FieldNotExist()

        data = FieldSettingAutocompleteSchema().dump(field)

        settings = SettingAutocompleteService.create(
            data_url=data_url,
            sheet=sheet,
            from_row=from_row,
            to_row=to_row,
            field_id=field.id)

        if settings is None:
            raise SettingAutocompleteNotExist()

        data['setting_autocomplete'] = {
            'data_url': settings.data_url,
            'sheet': settings.sheet,
            'from_row': settings.from_row,
            'to_row': settings.to_row
        }

        return data

    @staticmethod
    def _get_text_or_number_additional_options(field_id):
        """
        Check for choice additional options

        :param field_id:
        :return: dict
        """
        data = {}
        range_field = FieldRangeService.get_by_field_id(field_id)
        field = FieldService.get_by_id(field_id)

        if field.is_strict:
            data['is_strict'] = True

        if range_field:
            field_range = RangeService.get_by_id(range_field.range_id)
            if field_range:
                range_min = field_range.min
                range_max = field_range.max

                data['range'] = {
                    'min': range_min,
                    'max': range_max
                }

        return data

    @staticmethod
    def _get_choice_additional_options(field_id):
        """
        Check for choice additional options

        :param field_id:
        :return: dict
        """
        data = {}
        choice_options = ChoiceOptionService.filter(field_id=field_id)
        range_field = FieldRangeService.get_by_field_id(field_id)

        if choice_options:
            data['choice_options'] = []
            for option in choice_options:
                data['choice_options'].append(option.option_text)
        else:
            raise FieldNotExist('Choice Options Error')

        if range_field:
            field_range = RangeService.get_by_id(range_field.range_id)
            if field_range:
                range_min = field_range.min
                range_max = field_range.max

                data['range'] = {
                    'min': range_min,
                    'max': range_max
                }

        return data

    @staticmethod
    def _get_autocomplete_additional_options(field_id):
        """
        Check for autocomplete additional options

        :param field_id:
        :return: dict
        """
        data = {}
        settings_autocomplete = SettingAutocompleteService.get_by_field_id(field_id)

        if settings_autocomplete is None:
            raise SettingAutocompleteNotExist()

        data['setting_autocomplete'] = {
            'data_url': settings_autocomplete.data_url,
            'sheet': settings_autocomplete.sheet,
            'from_row': settings_autocomplete.from_row,
            'to_row': settings_autocomplete.to_row
        }

        return data

    @staticmethod
    def get_additional_options(field_id, field_type):
        """
        Check if field has other additional options

        :param field_id:
        :param field_type:
        :return: dict of options
        E.G. data = {'range' = {'min' : 0, 'max' : 100}
             data = {'choice_options' = ['man', 'woman']}
        """
        data = None

        try:
            if field_type in (FieldType.Number.value, FieldType.Text.value):
                data = FieldService._get_text_or_number_additional_options(field_id)

            elif field_type == FieldType.TextArea.value:
                data = {}

            elif field_type in (FieldType.Radio.value, FieldType.Checkbox.value):
                data = FieldService._get_choice_additional_options(field_id)

            elif field_type == FieldType.Autocomplete.value:
                data = FieldService._get_autocomplete_additional_options(field_id)

        except FieldNotExist():
            LOGGER.error('Couldn`t GET additional options')

        return data

    @staticmethod
    def check_for_range(data):
        """
        Check if range were send

        :param data: dict
        :return: range_min, range_max
        """
        range_min, range_max = None, None
        if range_instance := data.get('range'):
            range_min = range_instance.get('min')
            range_max = range_instance.get('max')
        return range_min, range_max

    @staticmethod
    @transaction_decorator
    def update_text_or_number_field(  # pylint: disable=too-many-arguments
            field_id,
            name,
            range_min,
            range_max,
            is_strict=False

    ):
        """
        Method to update field with number or text type.

        :param field_id: ID of the field that's being updated
        :param name: new name for the field
        :param is_strict: whether the field is restricted or not
        :param range_min: new minimum value for range object associated with the field
        :param range_max: new maximum value for range object associated with the field
        :return: json object with updated field
        """

        field = FieldService.update(
            field_id=field_id,
            name=name,
            is_strict=is_strict
        )
        data = FieldPutSchema().dump(field)
        field_range = FieldRangeService.get_by_field_id(field_id)

        if range_min is not None or range_max is not None:
            range_instance = RangeService.create(range_min=range_min, range_max=range_max)
            if field_range is not None:
                FieldRangeService.update(field_id=field_id, range_id=range_instance.id)
            else:
                FieldRangeService.create(field_id=field_id, range_id=range_instance.id)
        if field_range is not None:
            FieldRangeService.delete(field_id=field_id)

        return data

    @staticmethod
    @transaction_decorator
    def update_radio_field(
            field_id,
            name,
            added_choice_options=None,
            removed_choice_options=None,
            is_strict=False
    ):
        """
        Updates field with radio type

        :param field_id: id of the field object that's being updated
        :param name: updated name
        :param added_choice_options: choice options to add to the field
        :param removed_choice_options: choice options to remove from the field
        :param is_strict: whether the field has restrictions
        """
        field = FieldService.update(
            field_id=field_id,
            name=name,
            is_strict=is_strict
        )
        data = FieldPutSchema().dump(field)

        if added_choice_options:
            for added_option in added_choice_options:
                ChoiceOptionService.create(field_id=field_id, option_text=added_option)

        if removed_choice_options:
            for removed_option in removed_choice_options:
                option = ChoiceOptionService.get_by_field_and_text(field_id=field_id,
                                                                   option_text=removed_option)
                ChoiceOptionService.delete(option_id=option.id)

        return data

    @staticmethod
    @transaction_decorator
    def update_autocomplete_field(  # pylint: disable=too-many-arguments
            field_id,
            name,
            field_type,
            data_url,
            sheet,
            from_row,
            to_row
    ):
        """
        Update autocomplete field

        :param field_id:
        :param name:
        :param field_type: type of field
        :param data_url:
        :param sheet:
        :param from_row:
        :param to_row:
        :return:
        """

        field = FieldService.update(field_id=field_id, name=name)
        settings = SettingAutocompleteService.get_by_field_id(field_id)
        if settings is None:
            raise FieldNotExist()
        SettingAutocompleteService.update(
            setting_autocomplete_id=settings.id,
            data_url=data_url,
            sheet=sheet,
            from_row=from_row,
            to_row=to_row,
            field_id=field_id
        )
        data = FieldService.field_to_json(field)
        data['setting_autocomplete'] = FieldService.get_additional_options(field_id, field_type)

        return data

    @staticmethod
    @transaction_decorator
    def update_checkbox_field( # pylint: disable=too-many-arguments
            field_id,
            name,
            range_max,
            range_min,
            added_choice_options=None,
            removed_choice_options=None,
            is_strict=False
    ):
        """
        Method to update field with checkbox type

        :param field_id: id of the field object that's being updated
        :param name: updated name of the field
        :param range_max: maximum value of options that can be chosen
        :param range_min: minimum value of options that can be chosen
        :param added_choice_options: options to be added to the field
        :param removed_choice_options: options to be removed from the field
        :param is_strict: whether the field has restrictions
        """
        field = FieldService.update(
            field_id=field_id,
            name=name,
            is_strict=is_strict
        )
        data = FieldPutSchema().dump(field)
        field_range = FieldRangeService.get_by_field_id(field_id)

        if range_min is not None or range_max is not None:
            range_instance = RangeService.create(range_min=range_min, range_max=range_max)
            if field_range is not None:
                FieldRangeService.update(field_id=field_id, range_id=range_instance.id)
            else:
                FieldRangeService.create(field_id=field_id, range_id=range_instance.id)
        if field_range is not None:
            FieldRangeService.delete(field_id=field_id)

        if added_choice_options:
            for added_option in added_choice_options:
                ChoiceOptionService.create(field_id=field_id, option_text=added_option)

        if removed_choice_options:
            for removed_option in removed_choice_options:
                option = ChoiceOptionService.get_by_field_and_text(field_id=field_id,
                                                                   option_text=removed_option)
                ChoiceOptionService.delete(option_id=option.id)

        return data

    @staticmethod
    def check_form_membership(field_id):
        """
        Check if field is already contained in any form

        :param field_id: id of the field object
        :return: boolean value depending on whether the field is contained in form
        """
        field_in_form = FormFieldService.filter(field_id=field_id)
        return bool(field_in_form)
