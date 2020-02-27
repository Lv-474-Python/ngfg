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

    groups_users = DB.relationship('GroupUser', backref='group')


class BaseGroupSchema(MA.Schema):
    """
    Base group schema

    :param name - str
    :param owner_id - id
    """
    class Meta:
        """
        Base group schema meta
        """
        fields = ("id", "owner_id", "name")

    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)


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

    users_emails = fields.List(cls_or_instance=fields.Email, required=True)
