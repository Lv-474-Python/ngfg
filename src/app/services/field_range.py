"""
A service to handle FieldRange operations.
"""

from app.models.field_range import FieldRange
from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import FieldRangeNotExist


class FieldRangeService:
    """
    FieldRange service class.
    """

    @staticmethod
    @transaction_decorator
    def create(field_id, range_id):
        """
        FieldRange model create method

        :param field_id: id of the field object
        :param range_id: id of the range object
        :return: created FieldRange instance
        """
        field_range = FieldRange(field_id=field_id, range_id=range_id)
        DB.session.add(field_range)
        return field_range

    @staticmethod
    def get_by_field_id(field_id):
        """
        FieldRange model get by field id method

        :param field_id: id of the field object
        :return: FieldRange instance with specified id
        """
        field_range = FieldRange.query.filter(FieldRange.field_id == field_id).first()
        return field_range

    @staticmethod
    def filter(field_id, range_id):
        """
        FieldRange model filter method

        :param field_id: id of the field object
        :param range_id: id of the range object
        :return: list of FieldRange objects
        """
        filter_data = {}
        if field_id is not None:
            filter_data['field_id'] = field_id
        if range_id is not None:
            filter_data['range_id'] = range_id
        result = FieldRange.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def update(field_id, range_id=None):
        """
        FieldRange model update method

        :param field_id: id of the field object
        :param range_id: id of the range object
        :return: updated FieldRange instance or None
        """
        field_range = FieldRangeService.get_by_field_id(field_id)
        if not field_range:
            raise FieldRangeNotExist()
        if range_id is not None:
            field_range.range_id = range_id
        DB.session.merge(field_range)
        return field_range

    @staticmethod
    @transaction_decorator
    def delete(field_id):
        """
        FieldRange model delete method

        :param field_id: id of the field object
        :return: True if instance was deleted or None
        """
        field_range = FieldRangeService.get_by_field_id(field_id)
        if field_range is None:
            raise FieldRangeNotExist()
        DB.session.delete(field_range)
        return True
