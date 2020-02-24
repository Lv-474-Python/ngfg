from app.services import FieldService, FieldRangeService, RangeService, \
    ChoiceOptionService, SettingAutocompleteService
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType


class FieldPost:

    @staticmethod
    @transaction_decorator
    def create(name, owner_id, field_type, is_strict=False, **kwargs):
        Number = 1
        Text = 2
        TextArea = 3
        Radio = 4
        Autocomplete = 5
        Checkbox = 6

        field_instance = FieldService.create(name=name,
                                             owner_id=owner_id,
                                             field_type=field_type,
                                             is_strict=is_strict)
        instance_field_type = FieldType(field_type).name
        if field_type == Text:
            range_min = kwargs.get('range_min', 0)
            range_max = kwargs.get('range_max', 255)
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(field_instance.id, range_instance.id)
        elif field_type == Number:
            range_min = kwargs.get('range_min', -2_147_483_647)
            # max range will  be validated
            range_max = kwargs.get('range_max', 2_147_483_647)
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(field_instance.id, range_instance.id)
        elif field_type == Radio or field_type == Checkbox:
            choice_options = kwargs.get('choice_options')
            for option in choice_options:
                ChoiceOptionService.create(field_instance.id, option)

        elif field_type == Autocomplete:
            data_url = kwargs.get('data_url')
            sheet = kwargs.get('sheet')
            from_row = kwargs.get('from_row')
            to_row = kwargs.get('to_row')
            SettingAutocompleteService.create(data_url, sheet, from_row,
                                              to_row, field_instance)


    @staticmethod
    def check_other_options(field_id, field_type):
        """
        Check if field has other extra options

        :param field_id:
        :param field_type:
        :return: dict of options or None if field_type == TextArea
        """
        # CHANGE COPY PASTE
        Number = 1
        Text = 2
        TextArea = 3
        Radio = 4
        Autocomplete = 5
        Checkbox = 6

        data = {}

        if field_type == Number or field_type == Text:
            range_field = FieldRangeService.get_by_field_id(field_id)
            if range_field:
                ranges = RangeService.get_by_id(range_field.range_id)
                if ranges:
                    range_min = ranges.min
                    range_max = ranges.max


                    data['range_max'] = range_max
                    data['range_min'] = range_min



        elif field_type == TextArea:
            return None

        elif field_type == Radio or field_type == Checkbox:
            choice_options = ChoiceOptionService.filter(field_id=field_id)
            if choice_options:
                data['choice_options'] = []
                for option in choice_options:
                    data['choice_options'].append(option.option_text)

            print(data)

        return data


    @staticmethod
    def get(user_id):
        """
        Get list of user`s fields

        :param user_id:
        :return: list of fields
        """

        fields = FieldService.filter(owner_id=user_id)
        return fields
