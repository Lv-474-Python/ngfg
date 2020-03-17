"""
SharedField schemas
"""

from marshmallow import fields

from app import MA
from app.schemas import UserSchema, FieldPostSchema


class SharedFieldPostSchema(MA.Schema):
    """
    SharedField schema to use on POST request
    """
    class Meta:
        """
        Fields of SharedField schema to use on POST request
        """
        fields = ("recipients", "field_id")

    recipients = fields.List(fields.Email(), required=True)
    field_id = fields.Integer(required=True, data_key="fieldId")


class SharedFieldResponseSchema(MA.Schema):
    """
    SharedField schema used for response
    """
    class Meta:
        """
        Field of SharedField schema used for response
        """
        fields = ("user", "field")

    user = fields.Nested(UserSchema, required=True)
    field = fields.Nested(FieldPostSchema, required=True)
