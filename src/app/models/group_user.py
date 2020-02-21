"""
GroupUser model
"""

from app import DB
from .abstract_model import AbstractModel


class GroupUser(AbstractModel):
    """
    GroupUser model class

    :param user_id: id of the user that belongs to the group
    :param group_id: id of the group
    """

    __tablename__ = 'groups_users'
    __table_args__ = (
        DB.UniqueConstraint('user_id', 'group_id', name='unique_user_group'),
    )

    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    group_id = DB.Column(DB.Integer, DB.ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)
