"""
Field schemas
"""
from marshmallow import fields, validates_schema, ValidationError

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

    @validates_schema
    # pylint: disable=no-self-use
    def validate_field_type(self, data, **kwargs):
        """
        Validates incoming field type, and raises error if type is greater then 6 or lower than 1
        :param data:
        :param kwargs:
        :return: None or raise error
        """
        if data.get('field_type') > MAX_FIELD_TYPE or data.get('field_type') < MIN_FIELD_TYPE:
            raise ValidationError('Must be greater than or equal to 1 and less than or equal to 6.')


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
            "is_strict",
            "range",
            "added_choice_options",
            "removed_choice_options",
            "updated_autocomplete",
            "delete_range"
        )

    updated_name = fields.Str(required=False, data_key="updatedName")
    range = fields.Nested(RangeSchema)
    added_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="addedChoiceOptions"
    )
    removed_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="removedChoiceOptions"
    )
    updated_autocomplete = fields.Nested(
        SettingAutocompleteSchema,
        required=False,
        data_key="updatedAutocomplete"
    )
    delete_range = fields.Bool(required=False, data_key="deleteRange")
    is_strict = fields.Bool(required=False, data_key="isStrict")


class FieldNumberTextPutSchema(BasicField):
    """
    Field with type number or text schema on put request
    """

    class Meta:
        """
        Fields for field of type number or text schema meta on put request
        """
        fields = ("updated_name", "range", "is_strict", "delete_range")

    updated_name = fields.Str(required=False, data_key="updatedName")
    is_strict = fields.Boolean(required=False, data_key="isStrict")
    range = fields.Nested(RangeSchema, required=False)
    delete_range = fields.Boolean(required=False, data_key="deleteRange")


class FieldRadioPutSchema(BasicField):
    """
    Schema for field with radio type to use on put request
    """

    class Meta:
        """
        Fields for schema of field with radio type to use on put request
        """
        fields = ("updated_name", "added_choice_options", "removed_choice_options")

    updated_name = fields.Str(required=False, data_key="updatedName")
    added_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="addedChoiceOptions"
    )
    removed_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="removedChoiceOptions"
    )


class FieldCheckboxPutSchema(BasicField):
    """
    Schema for a field with checkbox type to use on put request
    """

    class Meta:
        """
        Fields for schema of field with checkbox type to use on put request
        """
        fields = (
            "updated_name",
            "range",
            "added_choice_options",
            "removed_choice_options",
            "delete_range"
        )

    updated_name = fields.Str(required=False, data_key="updatedName")
    range = fields.Nested(RangeSchema, required=False)
    added_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="addedChoiceOptions"
    )
    removed_choice_options = fields.List(
        fields.Str(),
        required=False,
        data_key="removedChoiceOptions"
    )


class FieldAutocompletePutSchema(BasicField):
    """
    Schema for a field with autocomplete type to use on put request
    """

    class Meta:
        """
        Fields for schema of field with autocomplete type to use on put request
        """
        fields = ("updated_name", "updated_autocomplete")

    updated_name = fields.Str(required=False, data_key="updatedName")
    updated_autocomplete = fields.Nested(
        SettingAutocompleteSchema,
        required=False,
        data_key="updatedAutocomplete"
    )


class FieldTextAreaPutSchema(BasicField):
    """
    Schema for a field with textarea type to use on put request
    """

    class Meta:
        """
        Fields for schema of field with textarea type to use on put request
        """
        fields = ("updated_name",)

    updated_name = fields.Str(required=False, data_key="updatedName")
