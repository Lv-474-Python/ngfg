"""abstract model"""
from sqlalchemy.exc import IntegrityError

from app import DB


class AbstractModel(DB.Model):
    """abstract model class"""

    __abstract__ = True

    id = DB.Column(DB.Integer, primary_key=True)
