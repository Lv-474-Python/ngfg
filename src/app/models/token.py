"""
Token model
"""
from app import DB
from .abstract_model import AbstractModel


class Token(AbstractModel):
    """
    Group model class

    :param form_id: to which form token generated
    :param token: generated token
    """

    __tablename__ = "tokens"

    token = DB.Column(DB.String(255), unique=True, nullable=False)
    form_id = DB.Column(DB.Integer, DB.ForeignKey('forms.id'), nullable=False)
    form_results = DB.relationship('FormResults', backref='token')
