from app.services import FieldService, FieldRangeService, RangeService, ChoiceOptionService, SettingAutocompleteService
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

        field_instance = FieldService.create(name=name, owner_id=owner_id, field_type=field_type, is_strict=is_strict)

        if field_type == Number or field_type == Text:
            range_min = kwargs.get('range_min', 0)
            range_max = kwargs.get('range_max', 255)
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(field_instance.id, range_instance.id)

        elif field_type == Radio or field_type == Checkbox:
            choice_options = kwargs.get('choice_options')
            print(choice_options)
            for option in choice_options:
                ChoiceOptionService.create(field_instance.id, option)

        elif field_type == Autocomplete:
            data_url = kwargs.get('data_url')
            sheet = kwargs.get('sheet')
            from_row = kwargs.get('from_row')
            to_row = kwargs.get('to_row')
            SettingAutocompleteService.create(data_url, sheet, from_row, to_row, field_instance)
