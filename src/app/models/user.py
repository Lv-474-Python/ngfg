"""
User model
"""

from flask_login import UserMixin
from app import DB
from .abstract_model import AbstractModel


class User(AbstractModel, UserMixin):
    '''
    User class
    '''

    __tablename__ = 'users'

    username = DB.Column(DB.String, unique=True, nullable=False)
    email = DB.Column(DB.String, unique=True, nullable=False)
    google_token = DB.Column(DB.Text, unique=True, nullable=False)

    @classmethod
    def get_by_google_token(cls, google_token):
        """
        Return user by google token
        :param google_token:
        :return:
        """
        user = cls.query.filter(cls.google_token == google_token).first()
        return user
