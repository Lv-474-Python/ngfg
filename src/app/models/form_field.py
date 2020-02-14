"""FormField model"""
from app import DB
from .abstract_model import AbstractModel


class FormField(AbstractModel):
    """FormField class"""

    __tablename__ = "form_fields"
    __table_args__ = (
        DB.UniqueConstraint('form_id', 'position', name='unique_form_position'),
    )

    form_id = DB.Column(DB.Integer, DB.ForeignKey('forms.id'), nullable=False)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id'), nullable=False)
    question = DB.Column(DB.Text, nullable=False)
    position = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f'form_id: {self.form_id}; field_id: {self.field_id}'
