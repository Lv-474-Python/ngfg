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
        fields = ("id", "owner_id", "name", "field_type")

    name = fields.Str(required=True)
    owner_id = fields.Integer(data_key="ownerId")
    field_type = fields.Integer(required=True, data_key="fieldType")

    @validates_schema
    def validate_field_type(self, data, **kwargs):
        if not (MIN_FIELD_TYPE <= data.get('field_type') <= MAX_FIELD_TYPE):
            raise ValidationError('Must be greater than or equal to 1 and less than or equal to 6.')


class FieldPostSchema(BasicField):
    """
    Field schema
    """

    class Meta:
        """
        Field schema meta
        """
        fields = ("owner_id", "name", "field_type", "is_strict", "range",
                  "setting_autocomplete", "choice_options")

    is_strict = fields.Boolean(data_key='isStrict')
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
        fields = ("id", "owner_id", "name", "field_type", "range", "is_strict")

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
