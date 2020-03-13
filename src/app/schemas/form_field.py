"""
FormField schemas
"""
from marshmallow import fields
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
        fields = ("id", "fieldId", "question", "position")

    field_id = fields.Integer(required=True, data_key="fieldId")
    question = fields.Str(required=True)
    position = fields.Integer(required=True, validate=Range(min=0))


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
