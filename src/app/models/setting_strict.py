""" Setting strict model"""
from app import DB
from .abstract_model import AbstractModel

class SettingStrict(AbstractModel):
    """
    Contains bool value if type is strict. Uses as validation to the user's answer.
    Strict text - only alpha
    Strict number - only integer
    :param is_strict: boolean value
    :param field_id: id of field that has this option

    """

    __tablename__ = 'settings_strict'
    __table_args__ = (
        DB.UniqueConstraint('field_id', name='unique_field'),
    )

    is_strict = DB.Column(DB.Boolean)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'Setting strict ID {self.id}, is strict? {self.is_strict}, Field ID {self.field_id}'