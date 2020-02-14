"""
ChoiceOption model
"""

from app import DB
from .abstract_model import AbstractModel

class ChoiceOption(AbstractModel):
    """
    ChoiceOption model class

    :param field_id: id of field that has this option
    :param option_text: choice option value
    """

    __tablename__ = 'choice_options'
    __table_args__ = (
        DB.UniqueConstraint('field_id', 'option_text', name='unique_field_option_text'),
    )

    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'))
    option_text = DB.Column(DB.Text, unique=False, nullable=False)

    def __repr__(self):
        return (f'<ChoiceOption {self.id}, text - {self.option_text}. Field {self.field.id}>')
