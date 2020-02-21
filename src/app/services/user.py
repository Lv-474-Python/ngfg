"""
User CRUD operations.
"""

from app import DB
from app.models import User
from app.helper.decorators import transaction_decorator
from app.helper.errors import UserNotExist


class UserService:
    """
    Class with user operations
    """

    @staticmethod
    @transaction_decorator
    def create(username, email, google_token):
        """
        Create new user in database

        :param username:
        :param email:
        :param google_token:
        :return: user or None
        """
        user = UserService.filter(email=email, google_token=google_token)

        if user:
            return user

        user = User(username=username, email=email, google_token=google_token)
        DB.session.add(user)
        return user

    @staticmethod
    @transaction_decorator
    def get_by_id(user_id):
        """
        Get user by id

        :param id:
        :return: user or none
        """
        user = User.query.get(user_id)
        return user

    @staticmethod
    @transaction_decorator
    def update(user_id, username=None, email=None, google_token=None):
        """
        Update user info in database

        :param user_id:
        :param username:
        :param email:
        :param google_token:
        :return: user or none
        """
        user = UserService.get_by_id(user_id)

        if user is None:
            raise UserNotExist()

        if username is not None:
            user.username = username

        if email is not None:
            user.email = email

        if google_token is not None:
            user.google_token = google_token

        DB.session.merge(user)
        return user

    @staticmethod
    @transaction_decorator
    def delete(user_id):
        """
        Delete user from database

        :param user_id:
        :return: True or None
        """
        user = UserService.get_by_id(user_id)

        if user is None:
            raise UserNotExist()

        DB.session.delete(user)
        return True

    @staticmethod
    @transaction_decorator
    def filter(username=None, email=None, google_token=None):
        """
        Check if user exist in database.

        :param username:
        :param email:
        :param google_token:
        :return: user or None
        """

        data = {}

        if username is not None:
            data['username'] = username

        if email is not None:
            data['email'] = email

        if google_token is not None:
            data['google_token'] = google_token

        user = User.query.filter_by(**data).all()

        return user
