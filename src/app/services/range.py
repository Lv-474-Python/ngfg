"""
Range service
"""
from sqlalchemy.exc import IntegrityError, ProgrammingError

from app import DB, LOGGER
from app.models import Range


class RangeService:
    """
    Class of range service
    """
    @staticmethod
    def create(min_value, max_value):
        """
        Creates Range object and saves if not created, or if created returns existing object
        :param min_value: int value
        :param max_value: int value
        :return: object of Range object
        """
        try:
            DB.session.begin(subtransactions=True)

            range_exist = Range.query.filter_by(min=min_value, max=max_value).first()
            if range_exist:
                return range_exist

            instance = Range(min=min_value, max=max_value)
            DB.session.add(instance)
            DB.session.commit()
            return instance
        except (IntegrityError, ProgrammingError) as error:
            LOGGER.error(f'{error}')
            DB.session.rollback()
            return None

    @staticmethod
    def delete(range_id):
        """
        Delete object with id param if exists
        :param range_id: int
        :return: True after deletion of None if object with id param doesn't exist
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = Range.query.get(range_id)
            if instance:
                DB.session.delete(instance)
                DB.session.commit()
                return True

            return None
        except (IntegrityError, ProgrammingError):
            DB.session.rollback()
            return None

    @staticmethod
    def update(range_id, min_value=None, max_value=None):
        """
        Updates object with id
        :param range_id:
        :param min_value: min value which can be changed
        :param max_value: max value which can be changed
        :return: object if changed, or None if object with id doesn't exist
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = Range.query.get(range_id)
            if instance:
                if min_value:
                    instance.min = min_value
                if max_value:
                    instance.max_restriction = max_value
                DB.session.commit()
                return instance

            return None
        except (IntegrityError, ProgrammingError):
            DB.session.rollback()
            return None
