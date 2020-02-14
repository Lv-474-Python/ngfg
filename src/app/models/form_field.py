"""FormField model"""
from app import DB
from .abstract_model import AbstractModel


class FormField(AbstractModel):
    """FormField class"""

    __tablename__ = "form_fields"
    __table_args__ = (
        DB.UniqueConstraint('form_id', 'position', name='unique_form_position'),
    )

    form_id = DB.Column(DB.Integer, DB.ForeignKey('form.id'), nullable=False)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('field.id'), nullable=False)
    question = DB.Column(DB.Text, nullable=False)
    position = DB.Column(DB.Integer, nullable=False)
