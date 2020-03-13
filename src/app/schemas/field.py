"""
Field schemas
"""
from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Range

from app import MA
from app.helper.constants import MAX_FIELD_TYPE, MIN_FIELD_TYPE
from app.schemas.range import RangeSchema
from app.schemas.setting_autocomplete import SettingAutocompleteSchema


class BasicField(MA.Schema):
    """
    Basic field schema (also used as TextAreas Schema)
    """

    class Meta:
        """
        Basic field schema meta
        """
        fields = ("owner_id", "name", "field_type")

    name = fields.Str(required=True)
    owner_id = fields.Integer(data_key="ownerId")
    field_type = fields.Integer(
        required=True,
        validate=Range(
            min=MIN_FIELD_TYPE,
            max=MAX_FIELD_TYPE
        ),
        data_key="fieldType"
    )


class FieldSchema(BasicField):
    """
    Field schema
    """

    class Meta:
        """
        Field schema meta
        """
        fields = ("id", "ownerId", "name", "fieldType", "isStrict", "range",
                  "settingAutocomplete", "choiceOptions")

    is_strict = fields.Boolean(required=False, data_key='isStrict')
    range = fields.Nested(RangeSchema)
    setting_autocomplete = fields.Nested(SettingAutocompleteSchema, data_key="settingAutocomplete")
    choice_options = fields.List(fields.Str(required=False), data_key="choiceOptions")


class FieldCheckboxSchema(BasicField):
    """
    Field with checkbox options and optional range
    """

    class Meta:
        """
        Field Checkbox Schema
        """
        fields = ("owner_id", "name", "field_type", "choice_options", "range")

    choice_options = fields.List(fields.Str(), required=True, data_key="choiceOptions")
    range = fields.Nested(RangeSchema, required=False)

    @validates_schema
    def validate_range_of_choices(self, data, **kwargs):
        """
        Validates range to choice_options amount
        :param data:
        :param kwargs:
        :return:
        """
        print(data)
        range_dict = data.get('range')
        options_list = data.get('choice_options')
        if range_dict:
            min_value = range_dict.get('min')
            max_value = range_dict.get('max')
            if min_value is not None:
                if min_value < 0:
                    raise ValidationError('Minimal selective options must be positive')
                if min_value > len(options_list):
                    raise ValidationError('Minimal selective options must\'t be greater than list of options')
            if max_value is not None:
                if max_value < 0:
                    raise ValidationError('Maximal selective options must be positive')
                if max_value > len(options_list):
                    raise ValidationError('Maximal selective options must\'t be greater than list of options')


class FieldRadioSchema(BasicField):
    """
    Field with choice options schema
    """

    class Meta:
        """
        Field with choice options schema meta
        """
        fields = ("owner_id", "name", "field_type", "choice_options")

    choice_options = fields.List(fields.Str(), required=True, data_key="choiceOptions")


class FieldNumberTextSchema(BasicField):
    """
    Field with type number or text schema
    """

    class Meta:
        """
        Field with type number or text schema meta
        """
        fields = ("id", "owner_id", "name", "field_type", "range", "isStrict")

    is_strict = fields.Boolean(required=False, data_key="isStrict")
    range = fields.Nested(RangeSchema, required=False)


class FieldSettingAutocompleteSchema(BasicField):
    """
    Field with autocomplete settings schema
    """

    class Meta:
        """
        Field with autocomplete settings schema meat
        """
        fields = ("owner_id", "name", "field_type", "setting_autocomplete")

    setting_autocomplete = fields.Nested(
        SettingAutocompleteSchema,
        required=True,
        data_key="settingAutocomplete"
    )


class FieldPutSchema(BasicField):
    """
    Field put schema
    """

    class Meta:
        """
        Field put schema meta
        """
        fields = (
            "updated_name",
            "range",
            "added_choice_options",
            "removed_choice_options",
            "updated_autocomplete"
        )

    updated_name = fields.Str(required=False)
    range = fields.Nested(RangeSchema, required=False)
    added_choice_options = fields.List(fields.Str(), required=False)
    removed_choice_options = fields.List(fields.Str(), required=False)
    updated_autocomplete = fields.Nested(SettingAutocompleteSchema, required=False)
