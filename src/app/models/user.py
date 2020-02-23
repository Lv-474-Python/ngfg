"""
User model
"""

from flask_login import UserMixin

from app import DB
from .abstract_model import AbstractModel


class User(AbstractModel, UserMixin):
    """
    User class
    """

    __tablename__ = 'users'

    username = DB.Column(DB.String, nullable=False)
    email = DB.Column(DB.String, unique=True, nullable=False)
    google_token = DB.Column(DB.Text, unique=True, nullable=False)

    forms = DB.relationship('Form', backref='owner')
    fields = DB.relationship('Field', backref='owner')
    shared_fields = DB.relationship('SharedField', backref='user')
    form_results = DB.relationship('FormResult', backref='user')
    groups = DB.relationship('Group', backref='user')
    groups_users = DB.relationship('GroupUser', backref='user')
