"""
Range service
"""
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError

from app import DB
from app.helper import transaction_decorator
from app.models import Range


class RangeService:
    """
    Class of range service
    """

    @staticmethod
    @transaction_decorator
    def create(min_value, max_value):
        """
        Creates Range object and saves if not created, or if created returns existing object
        :param min_value: int value
        :param max_value: int value
        :return: object of Range object
        """
        range_exist = Range.query.filter_by(min_value=min_value, max_value=max_value).first()
        if range_exist:
            return range_exist
        instance = Range(min_value=min_value, max_value=max_value)
        DB.session.add(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def update(range_id, min_value=None, max_value=None):
        """
        Updates object with id
        :param range_id:
        :param min_value: min value which can be changed
        :param max_value: max value which can be changed
        :return: object if changed, or None if object with id doesn't exist
        """
        instance = Range.query.get(range_id)
        if instance:
            if min_value is not None:
                instance.min_value = min_value
            if max_value is not None:
                instance.max_value = max_value
            DB.session.merge(instance)
            DB.session.commit()
            return instance
        return None

    @staticmethod
    @transaction_decorator
    def delete(range_id):
        """
        Delete object with id param if exists
        :param range_id: int
        :return: True after deletion of None if object with id param doesn't exist
        """
        instance = Range.query.get(range_id)
        if instance:
            DB.session.delete(instance)
            DB.session.commit()
            return True

    @staticmethod
    def get_by_id(range_id):
        instance = Range.query.get(range_id)
        return instance

    @staticmethod
    def filter(range_id=None, min_value=None, max_value=None):
        filter_data = {}
        if range_id is not None:
            filter_data['id'] = range_id
        if min_value is not None:
            filter_data['min_value'] = min_value
        if max_value is not None:
            filter_data['max_value'] = max_value
        result = Range.query.filter_by(**filter_data).all()
        return result
