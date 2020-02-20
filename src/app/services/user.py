"""
User CRUD operations.
"""

from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.models import User
from app import DB, LOGGER


class UserService:
    """
    Class with user`s CRUD operations
    """

    @staticmethod
    def create(username, email, google_token):
        """
        Create new user in database

        :param username:
        :param email:
        :param google_token:
        :return: user or None
        """
        try:
            DB.session.begin(subtransactions=True)

            user = User.query.filter_by(email=email).first()

            if user:
                return user

            if not user:
                user = User(username=username,
                            email=email,
                            google_token=google_token)
                DB.session.add(user)
                DB.session.commit()

        except IntegrityError as error:

            DB.session.rollback()
            LOGGER.warning(
                'IntegrityError happened: %s', error)
            return None

        return user

    @staticmethod
    def get_by_id(user_id):
        """
        Get user by id
        :param id:
        :return: user or none
        """
        try:
            user = User.query.get(user_id)
            return user

        except IntegrityError as error:
            LOGGER.warning(
                'Error happened: %s', error)
            return None

    @staticmethod
    def update(user_id, username=None, email=None, google_token=None):
        """
        Update user info in database

        :param username:
        :param email:
        :param google_token:
        :return:
        """
        try:
            DB.session.begin(subtransactions=True)

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
            DB.session.commit()

            return user

        except IntegrityError:
            DB.session.rollback()
            return None

    @staticmethod
    def delete(user_id):
        try:
            DB.session.begin(subtransactions=True)

            user = UserService.get_by_id(user_id)

            if user:
                DB.session.delete(user)
                DB.session.commit()
                return True

            if not user:
                LOGGER.warning(
                    'Someone tried to delete user with %s, but it doesn`t exist' % (user_id))
                return None

        except (IntegrityError, ProgrammingError) as error:
            LOGGER.warning(
                'Error happened: %s' % (error))
            DB.session.rollback()
            return None
