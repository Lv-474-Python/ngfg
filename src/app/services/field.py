"""
Field Service
"""
from sqlalchemy.exc import IntegrityError

from app import DB
from app.models import Field


class FieldService:
    """
    Field Service class
    """

    @staticmethod
    def create(name, owner_id, field_type):
        """
        Field model create method

        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :return: created field instance
        """

        try:
            DB.session.begin(subtransactions=True)

            instance = Field(name=name, owner_id=owner_id, field_type=field_type)

            DB.session.add(instance)
            DB.session.commit() # error is here

        except IntegrityError:
            DB.session.rollback()
            raise
        return instance

    @staticmethod
    def update(field_id, name=None, owner_id=None, field_type=None):  # pylint: disable=invalid-name
        """
        Field model update method

        :param field_id: field id
        :param name: field short name
        :param owner_id: field owner
        :param field_type: field type
        :return: updated field instance
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = Field.query.get(field_id)
            if name is not None:
                instance.name = name
            if owner_id is not None:
                instance.owner_id = owner_id
            if field_type is not None:
                instance.field_type = field_type

            DB.session.merge(instance)
            DB.session.commit()

        except IntegrityError:
            DB.session.rollback()
            raise
        return instance

    @staticmethod
    def delete(field_id):  # pylint: disable=invalid-name
        """
        Field model delete method

        :param field_id: field id
        :return: if field was deleted
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = Field.query.get(field_id)

            DB.session.delete(instance)
            DB.session.commit()

        except IntegrityError:
            DB.session.rollback()
            raise
        return True
