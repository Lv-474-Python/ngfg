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


class GroupSchema(MA.Schema):
    """
    Group schema
    """
    class Meta:
        """
        Group schema meta
        """
        fields = ("id", "name", "owner_id", "users")

    name = fields.Str(required=True)


class GroupPutSchema(GroupSchema):
    """
    GroupPut schema
    """
    class Meta:
        """
        GroupPut schema meta
        """
        fields = ("id", "name", "owner_id", "emails_add", "emails_delete", "users")

    emails_add = fields.List(fields.Email)
    emails_delete = fields.List(fields.Email)
