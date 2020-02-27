"""
ChoiceOption Service
"""
from app import DB
from app.models import ChoiceOption
from app.helper.decorators import transaction_decorator
from app.helper.errors import ChoiceOptionNotExist


class ChoiceOptionService:
    """
    ChoiceOption Service class
    """

    @staticmethod
    @transaction_decorator
    def create(field_id, option_text):
        """
        Create ChoiceOption instance

        :param field_id: id of field that has this option
        :param option_text: choice option value
        :return: created choice option instance
        """
        instance = ChoiceOption(field_id=field_id, option_text=option_text)
        options = ChoiceOptionService.filter(option_text=option_text)
        if options:
            return options[0]
        DB.session.add(instance)
        return instance

    @staticmethod
    def get_by_id(option_id):
        """
        Get ChoiceOption instance by id

        :param option_id: choice option id
        :return: ChoiceOption instance or None
        """
        instance = ChoiceOption.query.get(option_id)
        return instance

    @staticmethod
    def filter(option_id=None, field_id=None, option_text=None):
        """
        Filter ChoiceOption instances by id, field_id, option_text

        :param option_id: ChoiceOption id
        :param field_id: id of field that has this option
        :param option_text: ChoiceOption value
        :return: list of options
        """
        filter_data = {}
        if option_id is not None:
            filter_data['id'] = option_id
        if field_id is not None:
            filter_data['field_id'] = field_id
        if option_text is not None:
            filter_data['option_text'] = option_text

        result = ChoiceOption.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    @transaction_decorator
    def update(option_id, field_id=None, option_text=None):
        """
        Update ChoiceOption instance, got by option_id

        :param option_id: ChoiceOption id
        :param field_id: id of field that has this option
        :param option_text: ChoiceOption value
        :return: updated ChoiceOption instance
        """
        instance = ChoiceOptionService.get_by_id(option_id)
        if instance is None:
            raise ChoiceOptionNotExist()

        if field_id is not None:
            instance.field_id = field_id
        if option_text is not None:
            instance.option_text = option_text
        DB.session.merge(instance)
        return instance

    @staticmethod
    @transaction_decorator
    def delete(option_id):
        """
        Delete ChoiceOption instance

        :param option_id: ChoiceOption id
        :return: True - if field was deleted successfully, else - None
        """
        instance = ChoiceOptionService.get_by_id(option_id)
        if instance is None:
            raise ChoiceOptionNotExist()
        DB.session.delete(instance)
        return True

    @staticmethod
    def get_by_field_and_text(field_id, option_text):
        """
        Get ChoiceOption instance by field_id and text

        :param field_id: Field ID
        :param option_text: text of the option
        :return: ChoiceOption instance
        """

        instance = ChoiceOption.query.filter_by(field_id=field_id, option_text=option_text).first()
        return instance
