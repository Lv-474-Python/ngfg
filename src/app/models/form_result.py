"""
FormResult model
"""
from sqlalchemy import func

from app import DB
from .abstract_model import AbstractModel


class FormResult(AbstractModel):
    """
    FormResult model class
    :param user_id: user who answered to field
    :param answer: json {position: answer_id}
    :param token_id: id to table Tokens
    """
    __tablename__ = 'form_results'
    __table_args__ = (
        DB.UniqueConstraint('user_id', 'token_id', name='unique_user_token'),
    )

    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=True)
    answers = DB.Column(DB.JSON, nullable=False)
    token_id = DB.Column(DB.Integer, DB.ForeignKey('tokens.id'), nullable=False)
    created = DB.Column(DB.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return (f"<FormResult {self.id}, user: {self.user}, "
                f"answers: {self.answers}, token_id: {self.token.id}")
