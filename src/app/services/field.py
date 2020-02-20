"""
Field Service
"""
from app import DB
from app.models import Field
from app.helper.decorators import transaction_decorator
from app.helper.errors import FieldNotExist


class FieldService:
    """
    Field Service class
    """

    @staticmethod
    @transaction_decorator
    def create(name, owner_id, field_type):
        """
        Field model create method

        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :return: created field instance
        """

        instance = Field(name=name, owner_id=owner_id, field_type=field_type)
        DB.session.add(instance)
        return instance

    @staticmethod
    def get_by_id(field_id):
        """
        Field model get by id method

        :param id: field id
        :return: Field instance or None
        """
        instance = Field.query.get(field_id)
        return instance

    @staticmethod
    def filter(field_id=None, name=None, owner_id=None, field_type=None):
        """
        Field model filter method

        :param id: field id
        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :return: list of fields
        """
        filter_data = {}
        if id is not None:
            filter_data['id'] = field_id
        if name is not None:
            filter_data['name'] = name
        if owner_id is not None:
            filter_data['owner_id'] = owner_id
        if field_type is not None:
            filter_data['field_type'] = field_type

        result = Field.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def update(field_id, name=None, owner_id=None, field_type=None):
        """
        Field model update method

        :param field_id: field id
        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :return: updated field instance
        """
        instance = FieldService.get_by_id(field_id)
        if not instance:
            raise FieldNotExist()

        if name is not None:
            instance.name = name
        if owner_id is not None:
            instance.owner_id = owner_id
        if field_type is not None:
            instance.field_type = field_type
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def delete(field_id):
        """
        Field model delete method

        :param field_id: field id
        :return: if field was deleted
        """

        instance = FieldService.get_by_id(field_id)
        if not instance:
            raise FieldNotExist()
        DB.session.delete(instance)
        return True
