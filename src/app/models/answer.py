"""Answer model"""
from app import DB


class Answer(DB.Model):
    """Answer model class"""

    __tablename__ = 'answers'

    id = DB.Column(DB.Integer, primary_key=True)
    value = DB.Column(DB.Text, nullable=False, unique=True)
