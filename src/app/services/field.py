"""
Field Service
"""

from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import FieldNotExist, ChoiceNotSend
from app.models import Field, FieldSchema, RangeSchema, \
    SettingAutocompleteSchema
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
    @transaction_decorator
    def create_range(field_id, range_min, range_max):
        range_instance = RangeService.create(range_min, range_max)
        FieldRangeService.create(field_id=field_id, range_id=range_instance.id)
        return True

    @staticmethod
    @transaction_decorator
    def create_autocomplete_settings(field_id,
                                     data_url,
                                     sheet,
                                     from_row,
                                     to_row):

        SettingAutocompleteService.create(data_url, sheet, from_row,
                                          to_row, field_id)


    @staticmethod
    @transaction_decorator
    def create_text_or_number_field(name, owner_id, field_type,
                                    is_strict=False,
                                    range_min=None, range_max=None):

        field = FieldService.create(name=name,
                                    owner_id=owner_id,
                                    field_type=field_type,
                                    is_strict=is_strict)

        data = FieldSchema().dump(field)

        if range_min is not None or range_max is not None:
            range_instance = FieldService.create_range(field_id=field.id,
                                      range_min=range_min,
                                      range_max=range_max)
            data['range'] = RangeSchema.dump(range_instance)



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

        data = FieldSchema().dump(field)

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

        data = FieldSchema().dump(field)
        setting = SettingAutocompleteService.create(data_url=data_url,
                                          sheet=sheet,
                                          from_row=from_row,
                                          to_row=to_row,
                                          field_id=field.id)

        data['setting_autocomplete'] = SettingAutocompleteSchema().dump(setting)

        return data
