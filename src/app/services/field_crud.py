from app.services import FieldService, FieldRangeService, RangeService, \
    ChoiceOptionService, SettingAutocompleteService
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType


class FieldOperation:

    @staticmethod
    @transaction_decorator
    def create(name, owner_id, field_type, is_strict=False, **kwargs):
        
        field_instance = FieldService.create(name=name,
                                             owner_id=owner_id,
                                             field_type=field_type,
                                             is_strict=is_strict)

        name_of_field_type = FieldType(field_type).name

        if name_of_field_type == 'Text' or name_of_field_type :
            instance_range = kwargs.get('range', None)
            if instance_range is not None:
                range_min = instance_range.get('min', None)
                range_max = instance_range.get('max', None)
                range_instance = RangeService.create(range_min, range_max)
                FieldRangeService.create(field_instance.id, range_instance.id)

        elif name_of_field_type == 'Number':
            instance_range = kwargs.get('range', None)
            if instance_range is not None:
                range_min = instance_range.get('min', None)
                range_max = instance_range.get('max', None)
                range_instance = RangeService.create(range_min, range_max)
                FieldRangeService.create(field_instance.id, range_instance.id)

        elif name_of_field_type == 'Radio' or name_of_field_type == 'Checkbox':
            choice_options = kwargs.get('choice_options')
            for option in choice_options:
                ChoiceOptionService.create(field_instance.id, option)

        elif name_of_field_type == 'Autocomplete':
            setting_autocomplete = kwargs.get('setting_autocomplete')
            data_url = setting_autocomplete.get('data_url')
            sheet = setting_autocomplete.get('sheet')
            from_row = setting_autocomplete.get('from_row')
            to_row = setting_autocomplete.get('to_row')
            SettingAutocompleteService.create(data_url, sheet, from_row,
                                              to_row, field_instance.id)

    @staticmethod
    def check_other_options(field_id, field_type):
        """
        Check if field has other extra options

        :param field_id:
        :param field_type:
        :return: dict of options or None if field_type == TextArea
        E.G. data = {'range_max':250, 'range_min': 0}
             data = {'choice_options' = ['man', 'woman']}
        """
        name_of_field_type = FieldType(field_type).name
        
        data = {}

        if name_of_field_type == 'Number' or name_of_field_type == 'Text':
            range_field = FieldRangeService.get_by_field_id(field_id)
            if range_field:
                ranges = RangeService.get_by_id(range_field.range_id)
                if ranges:
                    range_min = ranges.min
                    range_max = ranges.max

                    data['range_max'] = range_max
                    data['range_min'] = range_min

        elif name_of_field_type == 'TextArea':
            return None

        elif name_of_field_type == 'Radio' or name_of_field_type == 'Checkbox':
            choice_options = ChoiceOptionService.filter(field_id=field_id)
            if choice_options:
                data['choice_options'] = []
                for option in choice_options:
                    data['choice_options'].append(option.option_text)

        # TODO
        elif name_of_field_type == 'Autocomplete':
            pass

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
