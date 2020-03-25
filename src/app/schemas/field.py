"""
Field schemas
"""
from marshmallow import fields, validates_schema, ValidationError

from app import MA
from app.helper.constants import MAX_FIELD_TYPE, MIN_FIELD_TYPE
from app.helper.choice_options_validator import check_for_repeated_options, check_for_same_options
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
        fields = ("id", "owner_id", "name", "field_type", "created")

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

    @validates_schema
    # pylint: disable=no-self-use
    def validate_choice_options(self, data, **kwargs):
        """
        Validates if choice options has repeated values
        :param data:
        :param kwargs:
        :return:
        """
        if check_for_repeated_options(options=data.get('choice_options')):
            raise ValidationError('Repeated values')


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
    # pylint:disable=no-self-use
    def validate_range_of_choices(self, data, **kwargs):
        """
        Validates range to choice_options amount
        :param data:
        :param kwargs:
        :return:
        """
        range_dict = data.get('range')
        options_list = data.get('choice_options')
        if range_dict:
            min_value = range_dict.get('min')
            max_value = range_dict.get('max')
            if min_value is not None:
                if min_value < 0:
                    raise ValidationError('Min selective options must be positive')
                if min_value > len(options_list):
                    raise ValidationError('Min selective options must be less than list of options')
            if max_value is not None:
                if max_value < 0:
                    raise ValidationError('Max selective options must be positive')
                if max_value > len(options_list):
                    raise ValidationError('Max selective options must be less than list of options')


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

    @validates_schema
    def validate_choice_options_repeats(self, data, **kwargs):
        added_options = data.get('added_choice_options')
        removed_options = data.get('removed_choice_options')
        if check_for_repeated_options(options=added_options):
            raise ValidationError('Repeated added values')
        if check_for_repeated_options(options=removed_options):
            raise ValidationError('Repeated removed values')
        if check_for_same_options(added=added_options, removed=removed_options):
            raise ValidationError('Identical values in added and removed options')

    @validates_schema
    def validate_new_or_deleted_range(self, data, **kwargs):
        new_range = data.get('range')
        delete_range = data.get('delete_range')
        if new_range and delete_range:
            raise ValidationError('Can\'t update and delete фе щту ешьу')


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
    delete_range = fields.Boolean(data_key='deleteRange')


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
