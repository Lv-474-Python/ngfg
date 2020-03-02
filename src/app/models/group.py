"""
Group model
"""
from marshmallow import fields

from app import DB, MA
from .abstract_model import AbstractModel


class Group(AbstractModel):
    """
    Group model class

    :param name: short name of the group
    :param owner_id: id of the user that created this group
    """

    __tablename__ = "groups"
    __table_args__ = (
        DB.UniqueConstraint('name', 'owner_id', name='unique_groupname_owner'),
    )

    name = DB.Column(DB.String, unique=False, nullable=False)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('users.id', ondelete="SET NULL"), nullable=False)

    groups_users = DB.relationship('GroupUser', backref='group', cascade='all,delete')


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
        fields = ("id", "name", "owner_id", "emails_add", "emails_delete", "users")

    emails_add = fields.List(cls_or_instance=fields.Email, required=True)
    emails_delete = fields.List(cls_or_instance=fields.Email, required=True)


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
