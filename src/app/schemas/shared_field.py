from marshmallow import fields

from app import MA
from app.schemas import UserSchema, FieldPostSchema


class SharedFieldSchema(MA.Schema):
    class Meta:
        fields = ("recipients", "field_id")

    recipients = fields.List(fields.Email(), required=True)
    field_id = fields.Integer(required=True, data_key="fieldId")


class SharedFieldResponseSchema(MA.Schema):
    class Meta:
        fields = ("user", "field")

    user = fields.Nested(UserSchema, required=True)
    field = fields.Nested(FieldPostSchema, required=True)
