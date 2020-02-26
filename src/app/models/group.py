"""
Group model
"""
from marshmallow import fields

from app import DB, MA
from .abstract_model import AbstractModel
from .user import UserSchema


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


class GroupScheme(MA.Schema):
    class Meta:
        """
        Group schema meta
        """
        fields = ("id", "name", "owner_id", "users")

    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    users = fields.List(fields.Nested(UserSchema))

