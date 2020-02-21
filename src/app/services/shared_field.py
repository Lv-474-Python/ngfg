"""
SharedField service
"""

from app import DB
from app.models import SharedField
from app.helper.decorators import transaction_decorator


class SharedFieldService:
    """
    SharedField Service class
    """

    @staticmethod
    @transaction_decorator
    def create(user_id, field_id):
        """
        SharedField model create method

        :param user_id: id of user object
        :param field_id: id of field object
        :return: created SharedField instance
        """

        shared_field = SharedField(user_id=user_id, field_id=field_id)
        DB.session.add(shared_field)
        return shared_field

    @staticmethod
    def get_by_id(user_id):
        """
        SharedField model get by id method

        :param user_id: id of the user object
        :return: SharedField instance with a specific id or None
        """

        shared_field = SharedField.query.filter(SharedField.user_id == user_id).first()
        return shared_field

    @staticmethod
    def filter(user_id=None, field_id=None):
        """
        SharedField model filter method

        :param user_id: id of the user object
        :param field_id: id of the field object
        :return: list of SharedField instances
        """
        filter_data = {}
        if user_id is not None:
            filter_data['user_id'] = user_id
        if field_id is not None:
            filter_data['field_id'] = field_id
        result = SharedField.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def delete(user_id):
        pass
