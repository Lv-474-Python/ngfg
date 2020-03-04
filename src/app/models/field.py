"""
Field model
"""
from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Range
from app import DB, MA
from app.helper.constants import MAX_FIELD_TYPE, MIN_FIELD_TYPE
from app.models.range import RangeSchema
from app.models.setting_autocomplete import SettingAutocompleteSchema
from .abstract_model import AbstractModel


class Field(AbstractModel):
    """
    Field model class

    :param name: short field name
    :param owner_id: id of user that created this field
    :param field_type: field type
    """

    __tablename__ = 'fields'
    __table_args__ = (
        DB.UniqueConstraint('name', 'owner_id', name='unique_name_owner'),
    )

    name = DB.Column(DB.String, unique=False, nullable=False)
    owner_id = DB.Column(
        DB.Integer,
        DB.ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
    field_type = DB.Column(DB.SmallInteger, unique=False, nullable=False)
    is_strict = DB.Column(DB.Boolean, default=False)

    choice_options = DB.relationship('ChoiceOption', cascade="all,delete", backref='field')
    shared_fields = DB.relationship('SharedField', backref='field')
    settings_autocomplete = DB.relationship(
        'SettingAutocomplete',
        cascade="all,delete",
        backref='field'
    )
    fields_range = DB.relationship('FieldRange', cascade="all,delete", backref='field')

    def __repr__(self):
        return (f'<Field {self.id}, name - {self.name}, '
                f'type - {self.field_type}, is_strict - {self.is_strict}>')


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
    owner_id = fields.Integer(required=True, data_key="ownerId")
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
