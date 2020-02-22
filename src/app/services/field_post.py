from app.services import FieldService, FieldRangeService, RangeService, ChoiceOptionService, SettingAutocompleteService
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType


class FieldPost:

    @staticmethod
    @transaction_decorator
    def create(name, owner_id, is_strict, field_type, **kwargs):
        # Number = 1
        # Text = 2
        # TextArea = 3
        # Radio = 4
        # Autocomplete = 5
        # Checkbox = 6
        a = {
            "name": "string",
            "owner_id": 0,
            "is_strict": False,
            "field_type": 1,  # number, string
            "range": {
                "min": 1,
                "max": 10}
        }
        field_instance = FieldService.create(name=name, owner_id=owner_id, field_type=field_type, is_strict=is_strict)

        if field_type == FieldType.Number or FieldType.Text:
            range_min = kwargs.get('range_min', 0)
            range_max = kwargs.get('range_max', 255)
            range_instance = RangeService.create(range_min, range_max)
            FieldRangeService.create(field_instance.id, range_instance.id)

