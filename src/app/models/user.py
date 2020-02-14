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

    def __init__(self, username, email, google_token):
        """

        :param username:
        :param email:
        :param google_token:
        """

        super().__init__(self)
        self.username = username
        self.email = email
        self.google_token = google_token
