"""
Answer service
"""

from app import DB
from app.helper.decorators import transaction_decorator
from app.models import Answer


class AnswerService:
    """
    Answer service class
    """

    @staticmethod
    def get_by_id(answer_id):
        """
        Get answer by id method

        :param answer_id:
        :return: answer with id=answer_id or None
        """
        answer = Answer.query.get(answer_id)
        return answer

    @staticmethod
    def get_by_value(value):
        """
        Get answer by value method

        :param value:
        :return: answer with value=value or None
        """
        answer = Answer.query.filter_by(value=value).first()
        return answer

    @staticmethod
    @transaction_decorator
    def create(value):
        """
        Answer create method

        :param value:
        :return: created answer instance
        """
        answer = Answer(value=value)
        DB.session.add(answer)
        return answer
