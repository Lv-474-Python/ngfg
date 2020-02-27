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
        answer = Answer.query.filter_by(value=str(value)).first()
        return answer

    @staticmethod
    @transaction_decorator
    def create(value):
        """
        Answer create method

        :param value: list or string
        :return: created or existing answer instance or list of instances
        """
        if not isinstance(value, list):
            answer = AnswerService.get_by_value(value)
            if answer is None:
                answer = Answer(value=str(value))
                DB.session.add(answer)
        else:
            answer = []
            for ans in value:
                if AnswerService.get_by_value(ans) is None:
                    new_ans = Answer(value=str(ans))
                    DB.session.add(new_ans)
                    answer.append(new_ans)
                else:
                    answer.append(AnswerService.get_by_value(ans))
        return answer
