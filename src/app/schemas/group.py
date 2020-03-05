"""
Group schemas
"""
from marshmallow import fields

from app import MA


class BaseGroupSchema(MA.Schema):
    """
    Base group schema
    """
    class Meta:
        """
        Base group schema meta
        """
        fields = ("id", "owner_id", "name")

    owner_id = fields.Int(dump_only=True, data_key='ownerId')
    name = fields.Str(required=True)


class GroupPutSchema(BaseGroupSchema):
    """
    GroupPut schema
    """
    class Meta:
        """
        GroupPut schema meta
        """
        fields = ("id", "name", "ownerId", "emails_add", "emails_delete", "users")

    emails_add = fields.List(
        cls_or_instance=fields.Email,
        required=False,
        data_key="emailsAdd")
    emails_delete = fields.List(
        cls_or_instance=fields.Email,
        required=False,
        data_key="emailsDelete")


class GroupPostSchema(BaseGroupSchema):
    """
    Group post schema

    :param users_emails - list of emails
    """
    class Meta:
        """
        Group post schema meta
        """
        fields = ("id", "owner_id", "name", "users_emails")

    users_emails = fields.List(cls_or_instance=fields.Email, required=True, data_key='usersEmails')
