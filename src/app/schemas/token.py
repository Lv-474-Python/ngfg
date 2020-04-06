"""
Token schemas
"""

from marshmallow import fields, validates_schema, ValidationError

from app import MA


class TokenSchema(MA.Schema):
    """
    Token schema
    """
    class Meta:
        """
        Fields of Token schema
        """
        fields = ("form_id", "group_id", "nbf", "exp")

    form_id = fields.Integer(required=True)
    group_id = fields.Integer(required=True, allow_none=True)
    nbf = fields.Integer(required=False)
    exp = fields.Integer(required=False)
