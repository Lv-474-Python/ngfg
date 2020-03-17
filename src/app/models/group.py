"""
Group model
"""
from sqlalchemy import func

from app import DB
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
    created = DB.Column(DB.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
