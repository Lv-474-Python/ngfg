"""
SharedField service
"""

from app import DB
from app.models import SharedField
from app.helper.decorators import transaction_decorator
from app.helper.errors import SharedFieldNotExist
from app.schemas import SharedFieldPostSchema, SharedFieldResponseSchema


class SharedFieldService:
    """
    SharedField Service class
    """

    @staticmethod
    @transaction_decorator
    def create(user_id, field_id, owner_id):
        """
        SharedField model create method

        :param user_id: id of user object
        :param field_id: id of field object
        :param owner_id: owner of the field that's being shared
        :return: created SharedField instance
        """

        shared_field = SharedField(user_id=user_id, field_id=field_id, owner_id=owner_id)
        DB.session.add(shared_field)
        return shared_field

    @staticmethod
    def get_by_id(shared_field_id):
        """
        SharedField model get by id method

        :param shared_field_id: id of the SharedField instance
        :return: SharedField instance with a specific id or None
        """

        shared_field = SharedField.query.get(shared_field_id)
        return shared_field

    @staticmethod
    def filter(shared_field_id=None, user_id=None, field_id=None, owner_id=None):
        """
        SharedField model filter method

        :param shared_field_id: is of the SharedField instance
        :param user_id: id of the user object
        :param field_id: id of the field object
        :param owner_id: owner of the field that's being shared
        :return: list of SharedField instances
        """
        filter_data = {}
        if shared_field_id is not None:
            filter_data['shared_field_id'] = shared_field_id
        if user_id is not None:
            filter_data['user_id'] = user_id
        if field_id is not None:
            filter_data['field_id'] = field_id
        if owner_id is not None:
            filter_data['owner_id'] = owner_id
        result = SharedField.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def delete(shared_field_id):
        """
        SharedField delete method

        :param shared_field_id: id of the SharedField instance
        :return: True if shared_field was deleted
        """

        shared_field = SharedFieldService.get_by_id(shared_field_id)
        if shared_field is None:
            raise SharedFieldNotExist()
        DB.session.delete(shared_field)
        return True

    @staticmethod
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = SharedFieldPostSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def response_to_json(data, many=False):
        """
        Get response data in json format
        """
        schema = SharedFieldResponseSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def get_by_user_and_field(user_id, field_id):
        """
        Get SharedField instance by user_id and field_id

        :param user_id: id of the user to whom the field was shared to
        :param field_id: id of the field that was shared
        :return: SharedField instance or None
        """
        shared_field_instance = SharedField.query.filter_by(
            user_id=user_id,
            field_id=field_id
        ).first()
        return shared_field_instance

    @staticmethod
    def validate_post_data(data):
        """
        Validate data by SharedFieldPostSchema
        """
        schema = SharedFieldPostSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)
