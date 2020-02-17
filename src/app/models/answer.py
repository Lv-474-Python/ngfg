"""Answer model"""
from app import DB
from .abstract_model import AbstractModel


class Answer(AbstractModel):
    """Answer model class"""

    __tablename__ = 'answers'

    value = DB.Column(DB.Text, nullable=False, unique=True)
