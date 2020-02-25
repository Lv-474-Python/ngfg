"""
Field Service
"""

from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.enums import FieldType
from app.helper.errors import FieldNotExist, ChoiceNotSend
from app.models import Field, FieldSchema, FieldNumberTextSchema, RangeSchema, \
    FieldSettingAutocompleteSchema, FieldChoiceOptionsSchema
from app.services.field_range import FieldRangeService
from app.services.range import RangeService
from app.services.choice_option import ChoiceOptionService
from app.services.setting_autocomplete import SettingAutocompleteService


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

        :param id: field id
        :return: Field instance or None
        """
        instance = Field.query.get(field_id)
        return instance

    @staticmethod
    def filter(field_id=None, name=None, owner_id=None, field_type=None,
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
    def update(field_id, name=None, owner_id=None, field_type=None,
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
    def validate(data):
        errors = FieldSchema().validate(data)
        return errors

    @staticmethod
    def validate_setting_autocomplete(data):
        errors = FieldSettingAutocompleteSchema().validate(data)
        return errors
    @staticmethod
    @transaction_decorator
    def create_range(field_id, range_min, range_max):
        range_instance = RangeService.create(range_min, range_max)
        FieldRangeService.create(field_id=field_id, range_id=range_instance.id)
        return True

    @staticmethod
    @transaction_decorator
    def create_text_or_number_field(name, owner_id, field_type,
                                    is_strict=False,
                                    range_min=None, range_max=None):

        field = FieldService.create(name=name,
                                    owner_id=owner_id,
                                    field_type=field_type,
                                    is_strict=is_strict)

        print('we are here1')
        print(field)
        data = FieldNumberTextSchema().dump(field)

        if range_min is not None or range_max is not None:
            print('we are here2')
            print(range_max, range_min)
            range_instance = FieldService.create_range(field_id=field.id,
                                      range_min=range_min,
                                      range_max=range_max)
            print(range_instance)

            data['range'] = {
                    'min': range_min,
                    'max': range_max
                }



        return data

    @staticmethod
    @transaction_decorator
    def create_choice_option_field(name, owner_id, field_type, is_strict=False,
                                   choice_options=None):

        if choice_options is None:
            raise ChoiceNotSend()

        field = FieldService.create(name=name,
                                    owner_id=owner_id,
                                    field_type=field_type,
                                    is_strict=is_strict)

        data = FieldChoiceOptionsSchema().dump(field)

        for option in choice_options:
            data['choice_options'].append(option)
            ChoiceOptionService.create(field.id, option)
        return data

    @staticmethod
    @transaction_decorator
    def create_autocomplete_field(name,
                                  owner_id,
                                  field_type,
                                  is_strict=False,
                                  data_url=None,
                                  sheet=None,
                                  from_row=None,
                                  to_row=None):

        field = FieldService.create(name=name,
                                    owner_id=owner_id,
                                    field_type=field_type,
                                    is_strict=is_strict)

        data = FieldSettingAutocompleteSchema().dump(field)
        SettingAutocompleteService.create(data_url=data_url,
                                          sheet=sheet,
                                          from_row=from_row,
                                          to_row=to_row,
                                          field_id=field.id)

        data['setting_autocomplete'] = {
            'data_url': data_url,
            'sheet': sheet,
            'from_row': from_row,
            'to_row': to_row
        }

        return data

    # YOI NAI BUDE
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

