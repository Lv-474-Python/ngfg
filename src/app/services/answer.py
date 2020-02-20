"""Answer service"""

from app import DB
from app.helper.decorators import transaction_decorator
from app.models import Answer


class AnswerService:
    """ answer service class"""

    @staticmethod
    def get_by_id(pk):
        """

        :param pk:
        :return: answer with id=pk or None

        """
        return Answer.query.get(pk)

    @staticmethod
    def get_by_value(value):
        """

        :param value:
        :return: answer with this value or None

        """
        return Answer.query.filter_by(value=value).first()

    @staticmethod
    @transaction_decorator
    def create(value):
        """

        :param value:
        :return: created answer instance
        """
        answer = Answer(value=value)
        DB.session.add(answer)
        return answer
