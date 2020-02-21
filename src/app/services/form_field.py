"""
FormField Service
"""
from app import DB
from app.models import FormField
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
    def filter(form_id=None, field_id=None, question=None, position=None):
        """

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
    def update(form_id, position, field_id=None, question=None):
        """

        :param form_id:
        :param position:
        :param field_id:
        :param question:
        :return: updated instance
        """
        instance = FormFieldService.filter(form_id=form_id, position=position).first()
        if instance is None:
            raise FormFieldNotExist()

        if field_id is not None:
            instance.field_id = field_id
        if question is not None:
            instance.question = question
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def delete(form_id, position):
        """

        :param form_id:
        :param position:
        :return: True if deleted
        """
        instance = FormFieldService.filter(form_id=form_id, position=position).first()
        if instance is None:
            raise FormFieldNotExist()
        DB.session.delete(instance)
        return True
