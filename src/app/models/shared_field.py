"""
SharedField model
"""

from app import DB
from .abstract_model import AbstractModel


class SharedField(AbstractModel):
    """
    SharedField model class

    :param user_id: id of a user to whom the field was shared to
    :param field_id: if of a field that has been shared
    """
    __tablename__ = "shared_fields"
    __table_args__ = (
        DB.UniqueConstraint('user_id', 'field_id', name='unique_user_field'),
    )

    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"SharedField {self.id}, field: {self.field_id}, user: {self.user_id}"
