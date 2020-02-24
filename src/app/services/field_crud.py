"""
Field operations
"""
from app.services import (FieldService, FieldRangeService, RangeService,
                          ChoiceOptionService, SettingAutocompleteService)
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType
from app.helper.errors import ChoiceNotSend, NotEnoughOptionsSend, SettingAutocompleteNotSend


class FieldOperation:
    """
    Field operations
    """
    @staticmethod
    @transaction_decorator
    # pylint: disable=too-many-locals
    def create(name, owner_id, field_type, is_strict=False, **kwargs):
        """
        Create field and other options in db

        :param name:
        :param owner_id:
        :param field_type:
        :param is_strict:
        :param kwargs: it may be:
            range={min,max},
            choice_options=['man', 'woman'],
            settings_autocomplete = {
                'data_url': 'http//...,
                'sheet': 'sheet name',
                'from_row': 'E1',
                'to_row': 'E25'
            }
        :return: dict
        """

        data = {}

        field_instance = FieldService.create(name=name,
                                             owner_id=owner_id,
                                             field_type=field_type,
                                             is_strict=is_strict)
        data['name'] = name
        data['owner_id'] = owner_id
        data['field_type'] = field_type
        data['is_strict'] = is_strict

        if field_type in (FieldType.Number.value, FieldType.Text.value):
            instance_range = kwargs.get('range', None)
            if instance_range is not None:
                range_min = instance_range.get('min', None)
                range_max = instance_range.get('max', None)
                range_instance = RangeService.create(range_min, range_max)
                FieldRangeService.create(field_instance.id, range_instance.id)

                data['range'] = {
                    'min': range_min,
                    'max': range_max
                }

        elif field_type in (FieldType.Radio.value, FieldType.Checkbox.value):
            data['choice_options'] = []
            choice_options = kwargs.get('choice_options', None)
            if choice_options is None:
                raise ChoiceNotSend()

            if field_type == FieldType.Radio.value and len(choice_options) < 2 or \
                    field_type == FieldType.Checkbox.value and len(choice_options) < 1:
                raise NotEnoughOptionsSend()

            for option in choice_options:
                data['choice_options'].append(option)
                ChoiceOptionService.create(field_instance.id, option)

        elif field_type == FieldType.Autocomplete.value:
            setting_autocomplete = kwargs.get('setting_autocomplete', None)
            if setting_autocomplete is None:
                raise SettingAutocompleteNotSend()

            data_url = setting_autocomplete.get('data_url')
            sheet = setting_autocomplete.get('sheet')
            from_row = setting_autocomplete.get('from_row')
            to_row = setting_autocomplete.get('to_row')
            SettingAutocompleteService.create(data_url, sheet, from_row,
                                              to_row, field_instance.id)

            data['setting_autocomplete'] = {
                'data_url': data_url,
                'sheet': sheet,
                'from_row': from_row,
                'to_row': to_row
            }

        return data

    @staticmethod
    def check_other_options(field_id, field_type):
        """
        Check if field has other extra options

        :param field_id:
        :param field_type:
        :return: dict of options or None
        E.G. data = {'range' = {'min' : 0, 'max' : 100}
             data = {'choice_options' = ['man', 'woman']}
        """

        data = {}

        if field_type in (FieldType.Number.value, FieldType.Text.value):
            range_field = FieldRangeService.get_by_field_id(field_id)

            field = FieldService.get_by_id(field_id)
            if field.is_strict:
                data['is_strict'] = True

            if range_field:
                ranges = RangeService.get_by_id(range_field.range_id)
                if ranges:
                    range_min = ranges.min
                    range_max = ranges.max

                    data['range'] = {
                        'min': range_min,
                        'max': range_max
                    }

        elif field_type == FieldType.TextArea.value:
            return None

        elif field_type in (FieldType.Radio.value, FieldType.Checkbox.value):
            choice_options = ChoiceOptionService.filter(field_id=field_id)
            if choice_options:
                data['choice_options'] = []
                for option in choice_options:
                    data['choice_options'].append(option.option_text)

        elif field_type == FieldType.Autocomplete.value:
            settings_autocomplete = SettingAutocompleteService.filter(
                field_id=field_id)
            if settings_autocomplete:
                settings_autocomplete = settings_autocomplete[0]
            else:
                return None

            data['setting_autocomplete'] = {
                'data_url': settings_autocomplete.data_url,
                'sheet': settings_autocomplete.sheet,
                'from_row': settings_autocomplete.from_row,
                'to_row': settings_autocomplete.to_row
            }

        return data

    @staticmethod
    def get_user_fields(user_id):
        """
        Get list of user`s fields

        :param user_id:
        :return: list of fields
        """
        fields = FieldService.filter(owner_id=user_id)
        return fields
