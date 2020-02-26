"""
FormField Service
"""
from app import DB
from app.models import FormField, FormFieldSchema
from app.helper.decorators import transaction_decorator
from app.helper.errors import FormFieldNotExist


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
        return instance

    @staticmethod
    @transaction_decorator
    def get_by_id(form_field_id):
        """
        Get FormField by id

        :param form_field_id:
        :return: form or none
        """
        form_field = FormField.query.get(form_field_id)
        return form_field

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
        result = FormField.query.filter_by(**filter_data).all()
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
    def to_json(data, many):
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

    @staticmethod
    def validate_position(data):
        """
        Validate position value
        """
