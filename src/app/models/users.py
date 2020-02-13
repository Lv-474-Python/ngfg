'''
User model
'''

from flask_login import UserMixin
from app import DB


class User(DB.Model, UserMixin):
    '''
    User class
    '''
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    username = DB.Column(DB.String, unique=True, nullable=False)
    email = DB.Column(DB.String, unique=True, nullable=False)
    google_token = DB.Column(DB.Text, unique=True, nullable=False)

    def __init__(self, username, email, google_token):
        '''

        :param username:
        :param email:
        :param google_token:
        '''
        self.username = username
        self.email = email
        self.google_token = google_token

    @staticmethod
    def create(username, email, google_token):
        """

        :param username:
        :param email:
        :param google_token:
        :return:
        """
        user = User(username, email, google_token)
        DB.session.add(user)
        DB.session.commit()
        return user
