"""
User CRUD operations.
"""

from app import DB
from app.models import User
from app.helper.decorators import transaction_decorator


class UserService:
    """
    Class with user`s CRUD operations
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
        user = User.query.filter_by(email=email).first()

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

        :param username:
        :param email:
        :param google_token:
        :return: user or none
        """
        user = UserService.get_by_id(user_id)

        if not user:
            return None

        if username:
            user.username = username

        if email:
            user.email = email

        if google_token:
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

        if user:
            DB.session.delete(user)
            return True

        return None
