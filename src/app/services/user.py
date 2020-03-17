"""
User CRUD operations.
"""

from app import DB, LOGIN_MANAGER
from app.models import User
from app.schemas import UserSchema
from app.helper.decorators import transaction_decorator
from app.helper.errors import UserNotExist, UserNotCreated


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
        user = UserService.filter(email=email)

        if user:
            return user[0]

        user = User(username=username, email=email, google_token=google_token)
        DB.session.add(user)
        return user

    @staticmethod
    @LOGIN_MANAGER.user_loader
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
    def update(user_id, username=None, email=None, google_token=None, is_active=None):
        """
        Update user info in database

        :param user_id:
        :param username:
        :param email:
        :param google_token:
        :param is_active:
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
        if is_active is not None:
            user.is_active = is_active

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
    def filter(username=None, email=None, google_token=None, is_active=None):
        """
        Check if user exist in database.

        :param username:
        :param email:
        :param google_token:
        :param is_active:
        :return: user or None
        """

        data = {}

        if username is not None:
            data['username'] = username
        if email is not None:
            data['email'] = email
        if google_token is not None:
            data['google_token'] = google_token
        if is_active is not None:
            data['is_active'] = is_active

        users = User.query.filter_by(**data).all()

        return users

    @staticmethod
    @transaction_decorator
    def activate_user(user_id, username, google_token):
        """
        Activates user
        :param user_id:
        :param username:
        :param google_token:
        :return: user or None
        """
        user = UserService.get_by_id(user_id)
        if user is None:
            raise UserNotExist()
        user = UserService.update(
            user.id,
            username=username,
            google_token=google_token,
            is_active=True
        )
        # DB.session.merge(user)
        return user

    @staticmethod
    def to_json(data):
        """
        Get data in json format
        """
        schema = UserSchema()
        return schema.dump(data)

    @staticmethod
    @transaction_decorator
    def create_user_by_email(email):
        """
        Create new user in database by email

        :param email: user email
        :return: user or None
        """
        users = UserService.filter(email=email)

        if users:
            return users[0]

        user = User(email=email)
        DB.session.add(user)
        return user

    @staticmethod
    @transaction_decorator
    def create_users_by_emails(emails):
        """
        Having list of emails create users

        :param emails: list of emails
        :return: list of users
        """
        users = []
        for email in emails:
            user = UserService.create_user_by_email(email)
            if user is None:
                raise UserNotCreated()
            users.append(user)
        return users

    @staticmethod
    def get_by_email(email):
        """
        Get user by email

        :param email: email to get user by
        :return: User instance or None
        """
        user = User.query.filter_by(email=email).first()
        return user
