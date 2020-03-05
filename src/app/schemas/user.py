"""
User schemas
"""
from marshmallow import fields

from app import MA


class UserSchema(MA.Schema):
    """
    User schema

    """
    class Meta:
        """
        User schema meta
        """
        fields = ("id", "username", "email", "is_active")

    is_active = fields.Bool(dump_only=True, data_key='isActive')
