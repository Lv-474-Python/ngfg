"""
Range service
"""
from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import RangeNotExist
from app.models import Range


class RangeService:
    """
    Class of range service
    """

    @staticmethod
    @transaction_decorator
    def create(range_min, range_max):
        """
        Creates Range object and saves if not created, or if created returns existing object

        :param range_min: int value
        :param range_max: int value
        :return: created object of Range object or returns existing
        """
        range_exist = Range.query.filter_by(min=range_min, max=range_max).first()
        if range_exist:
            return range_exist
        instance = Range(min=range_min, max=range_max)
        DB.session.add(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def update(range_id, range_min=None, range_max=None):
        """
        Updates object with id

        :param range_id:
        :param range_min: min value which can be changed
        :param range_max: max value which can be changed
        :return: object if changed, or None if object with id doesn't exist
        """
        instance = RangeService.get_by_id(range_id)
        if instance is None:
            raise RangeNotExist()

        if range_min is not None:
            instance.min = range_min
        if range_max is not None:
            instance.max = range_max
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def delete(range_id):
        """
        Delete object with id param if exists

        :param range_id: int
        :return: True after deletion of None if object with id param doesn't exist
        """
        instance = RangeService.get_by_id(range_id)
        if instance is None:
            raise RangeNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    def get_by_id(range_id):
        """
        Get Range model object by id

        :param range_id: id of range
        :return: Range instance or None
        """
        instance = Range.query.get(range_id)
        return instance

    @staticmethod
    def filter(range_id=None, range_min=None, range_max=None):
        """
        Filter method

        :param range_id: range id
        :param range_min: range int of min value
        :param range_max: range int of max value
        :return: list of range objects
        """
        filter_data = {}
        if range_id is not None:
            filter_data['id'] = range_id
        if range_min is not None:
            filter_data['min'] = range_min
        if range_max is not None:
            filter_data['max'] = range_max
        result = Range.query.filter_by(**filter_data).all()
        return result
