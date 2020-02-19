"""
ChoiceOption Service
"""
from sqlalchemy.exc import IntegrityError

from app import DB
from app.models import ChoiceOption


class ChoiceOptionService:
    """
    ChoiceOption Service class
    """

    @staticmethod
    def create(field_id, option_text):
        """
        ChoiceOption model create method

        :param field_id: id of field that has this option
        :param option_text: choice option value
        :return: created choice option instance
        """

        try:
            DB.session.begin(subtransactions=True)

            instance = ChoiceOption(field_id=field_id, option_text=option_text)

            DB.session.add(instance)
            DB.session.commit() # error is here

        except IntegrityError:
            DB.session.rollback()
            raise
        return instance

    @staticmethod
    def update(choice_option_id, field_id=None, option_text=None):
        """
        ChoiceOption model update method

        :param choice_option_id: choice option id
        :param field_id: id of field that has this option
        :param option_text: choice option value
        :return: updated choice option instance
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = ChoiceOption.query.get(choice_option_id)
            if field_id is not None:
                instance.field_id = field_id
            if option_text is not None:
                instance.option_text = option_text

            DB.session.merge(instance)
            DB.session.commit()

        except IntegrityError:
            DB.session.rollback()
            raise
        return instance

    @staticmethod
    def delete(choice_option_id):
        """
        ChoiceOption model delete method

        :param choice_option_id: choice option id
        :return: if field was deleted
        """
        try:
            DB.session.begin(subtransactions=True)

            instance = ChoiceOption.query.get(choice_option_id)

            DB.session.delete(instance)
            DB.session.commit()

        except IntegrityError:
            DB.session.rollback()
            raise
        return True
