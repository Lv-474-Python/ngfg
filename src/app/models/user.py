'''
User model
'''

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

    fields = DB.relationship('Field', backref='owner')
