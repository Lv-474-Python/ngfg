"""
FormField schemas
"""
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Range

from app import MA
from .field import FieldPostSchema


class FormFieldSchema(MA.Schema):
    """
    FormField schema
    """
    class Meta:
        """
        FormField fields to expose
        """
        fields = ("id", "field_id", "question", "position")

    field_id = fields.Integer(required=True, data_key="fieldId")
    question = fields.Str(required=True)
    position = fields.Integer(required=True, validate=Range(min=0))

    @validates("question")
    def validate_question(self, value):
        if value == "":
            raise ValidationError("Missing data for required field.")
        if value.lower() == "token":
            raise ValidationError("This value is not allowed.")


class FormFieldResponseSchema(MA.Schema):
    """
    FormField put schema
    """
    class Meta:
        """
        Fields of the put schema
        """
        fields = ("id", "field", "question", "position")

    field = fields.Nested(FieldPostSchema, required=True)
    question = fields.Str(required=True)
    position = fields.Integer(required=True, validate=Range(min=0))
