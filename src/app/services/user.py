from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app.models import User
from app import DB, LOGGER


class UserService:

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
            LOGGER.warning(
                f'IntegrityError happened: {error}')
            return None

        return user

    # TODO
    def update(self, username=None, email=None, google_token=None):
        """
        Update user info in database

        :param username:
        :param email:
        :param google_token:
        :return:
        """
        if username:
            self.username = username
        if email:
            self.email = email

        if google_token:
            self.google_token = google_token

    @staticmethod
    def delete(id):
        try:
            user = User.query.get(id)
            print(type(user))

            if user:
                DB.session.delete(user)
                DB.session.commit()

            if not user:
                LOGGER.warning(
                    f'Someone tried to delete user with {id=}, but it doesn`t exist')
                return None

        except (IntegrityError, ProgrammingError):
            LOGGER.warning(
                f'Error happened: {IntegrityError}')
            return None
