"""
FormResult model
"""

from sqlalchemy import func
from app import DB
from app import MA
from .abstract_model import AbstractModel


class FormResult(AbstractModel):
    """
    FormResult model class
    :param user_id: user who answered to field
    :param answer: json {position: answer_id}
    :param form_id: id to table Form
    """
    __tablename__ = 'form_results'

    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'),
                        nullable=False)
    answers = DB.Column(DB.JSON, nullable=False)
    form_id = DB.Column(DB.Integer, DB.ForeignKey('forms.id'),
                        nullable=False)
    created = DB.Column(DB.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (f"<FormResult {self.id}, user: {self.user.id}, "
                f"answer: {self.answers}, form_id: {self.form.id}")


class FormResultSchema(MA.SQLAlchemyAutoSchema):
    """
    FormResult marshmallow schema
    """
    class Meta:
        """
        Schema meta
        """
        model = FormResult
        include_fk = True
