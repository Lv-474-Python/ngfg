"""
FormField Service
"""
from app import DB
from app.models import FormField
from app.helper.decorators import transaction_decorator
from app.helper.errors import FormFieldNotExist
from app.schemas import FormFieldSchema
from app.helper.redis_manager import RedisManager


class FormFieldService:
    """
    FormField Service class
    """

    @staticmethod
    @transaction_decorator
    def create(form_id, field_id, question, position):
        """
        Create FormField method

        :param form_id:
        :param field_id:
        :param question:
        :param position:
        :return: created FormField instance
        """
        instance = FormField(form_id=form_id,
                             field_id=field_id,
                             question=question,
                             position=position)
        DB.session.add(instance)

        key = f'form_fields:form_id:{form_id}'
        result = RedisManager.get(key, 'data')
        if result is not None:
            RedisManager.delete(key)

        return instance

    @staticmethod
    @transaction_decorator
    def get_by_id(form_field_id):
        """
        Get FormField by id

        :param form_field_id:
        :return: form or none
        """
        result = RedisManager.get(f'form_field:{form_field_id}', 'data')

        if result is None:
            result = FormField.query.get(form_field_id)
            RedisManager.set(f'form_field:{form_field_id}', result)

        return result

    @staticmethod
    def filter(form_id=None, field_id=None, question=None, position=None):
        """
        Filter FormField method

        :param form_id:
        :param field_id:
        :param question:
        :param position:
        :return: FormField list
        """
        filter_data = {}
        if form_id is not None:
            filter_data['form_id'] = form_id
        if field_id is not None:
            filter_data['field_id'] = field_id
        if position is not None:
            filter_data['position'] = position
        if question is not None:
            filter_data['question'] = question

        key = RedisManager.generate_key('form_fields:', filter_data)
        result = RedisManager.get(key, 'data')

        if result is None:
            result = FormField.query.filter_by(**filter_data).all()
            RedisManager.set(key, result)
        return result

    @staticmethod
    @transaction_decorator
    def update(form_field_id, form_id=None, position=None, field_id=None, question=None):
        """
        Update FormField method

        :param form_field_id:
        :param form_id:
        :param position:
        :param field_id:
        :param question:
        :return: updated FormField
        """
        instance = FormFieldService.get_by_id(form_field_id)
        if instance is None:
            raise FormFieldNotExist()

        if form_id is not None:
            instance.form_id = form_id
        if position is not None:
            instance.position = position
        if field_id is not None:
            instance.field_id = field_id
        if question is not None:
            instance.question = question
        DB.session.merge(instance)

        # delete object cache
        key = f'form_field:{form_field_id}'
        result = RedisManager.get(key, 'data')
        if result is not None:
            RedisManager.delete(key)

        # delete list cache with this object
        key = f'form_fields:form_id:{form_id}'
        result = RedisManager.get(key, 'data')
        if result is not None:
            RedisManager.delete(key)

        return instance

    @staticmethod
    @transaction_decorator
    def delete(form_field_id):
        """
        FormField delete method

        :param form_field_id:
        :return: True if deleted
        """
        instance = FormFieldService.get_by_id(form_field_id)
        if instance is None:
            raise FormFieldNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    def to_json(data, many=False):
        """
        A method to get object data in json format
        """
        form_field_schema = FormFieldSchema(many=many)
        return form_field_schema.dump(data)

    @staticmethod
    def validate_data(data):
        """
        Validate data with FormFieldSchema
        """
        schema = FormFieldSchema()
        errors = schema.validate(data)
        return not bool(errors), errors
