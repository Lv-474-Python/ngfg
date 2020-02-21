"""
FormResult service
"""

from app.models import FormResult
from app import DB
from app.helper.decorators import transaction_decorator


class FormResultService:
    """
    Class for SettingAutocomplete service
    """
    @staticmethod
    @transaction_decorator
    def create(user_id, form_id, answer):
        """
        Create FormResult model

        :param user_id:
        :param form_id:
        :param answer:
        :return:
        """

        form_result = FormResult(
            user_id=user_id,
            form_id=form_id,
            answer=answer
        )

        DB.session.add(form_result)
        return form_result

    @staticmethod
    def get_by_id(form_result_id):
        """
        Get FormResult model by id

        :param form_result_id:
        :return: FormResult object or None
        """

        setting_autocomplete = FormResult.query.get(form_result_id)
        return setting_autocomplete

    @staticmethod
    def filter(form_result_id=None, user_id=None, form_id=None, answer=None):
        """
        FormResult filter method

        :param form_result_id:
        :param user_id:
        :param form_id:
        :param answer:
        :return: list of FormResult objects or empty list
        """
        filter_data = {}

        if form_result_id is not None:
            filter_data['id'] = form_result_id
        if user_id is not None:
            filter_data['user_id'] = user_id
        if form_id is not None:
            filter_data['form_id'] = form_id
        if answer is not None:
            filter_data['answer'] = answer

        result = FormResult.query.filter_by(**filter_data).all()
        return result
