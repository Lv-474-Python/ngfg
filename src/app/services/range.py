"""
Range service
"""
from sqlalchemy.exc import IntegrityError

from app import DB
from app.models import Range


class RangeService:
    @staticmethod
    def create(min, max):
        """
        Creates Range object and saves if not created, or if created returns existing object
        :param min: int value
        :param max: int value
        :return: object of Range object
        """
        try:
            range_exist = Range.query.filter_by(min=min, max=max).first()
            if range_exist:
                return range_exist
            else:
                instance = Range(min=min, max=max)
                DB.session.add(instance)
                DB.session.commit()
                return instance
        except IntegrityError:
            DB.session.rollback()
            return None

    @staticmethod
    def delete(id):
        """
        Delete object with id param if exists
        :param id: int
        :return: True after deletion of None if object with id param doesn't exist
        """
        try:
            instance = Range.query.get(id)
            if instance:
                DB.session.delete(instance)
                DB.session.commit()
                return True
            else:
                return None
        except IntegrityError:
            DB.session.rollback()
            return None

    @staticmethod
    def update(id, min=None, max=None):
        """
        Updates object with id
        :param id:
        :param min: min value which can be changed
        :param max: max value which can be changed
        :return: object if changed, or None if object with id doesn't exist
        """
        try:
            instance = Range.query.get(id)
            if instance:
                if min:
                    instance.min = min
                if max:
                    instance.max = max
                DB.session.commit()
                return instance
            else:
                return None
        except IntegrityError:
            DB.session.rollback()
            return None
