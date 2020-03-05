"""
FormField schemas
"""
from marshmallow import fields
from marshmallow.validate import Range

from app import MA


class FormFieldSchema(MA.Schema):
    """
    FormField schema
    """
    class Meta:
        """
        FormField fields to expose
        """
        fields = ("id", "field_id", "question", "position")

    field_id = fields.Integer(required=True)
    question = fields.Str(required=True)
    position = fields.Integer(required=True, validate=Range(min=0))
