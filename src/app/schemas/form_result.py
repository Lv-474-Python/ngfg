"""
FormResult schemas
"""
from marshmallow import fields, ValidationError

from app import MA


class Keys(fields.Field):
    """
    Custom field to check answers dict keys
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserialization method

        :param value:
        :param attr:
        :param data:
        :param kwargs:
        :return:
        """
        if value not in ("position", "answer"):
            raise ValidationError("Wrong answer key")
        return value


class FormResultPostSchema(MA.Schema):
    """
    FormResult marshmallow schema
    """
    class Meta:
        """
        Schema meta
        """
        fields = ("id", "user_id", "form_id", "created", "answers")

    answers = fields.List(fields.Dict(keys=Keys, values=fields.Raw()))


class FormResultGetSchema(MA.Schema):
    """
    FormResult marshmallow schema
    """
    class Meta:
        """
        Schema meta
        """
        fields = ("id", "user_id", "form_id", "created", "answers")

    answers = fields.Dict(required=True, keys=fields.String(), values=fields.Raw())
    user_id = fields.Integer(data_key="userId")
    form_id = fields.Integer(data_key="formId")
