"""Answer model"""
from app import DB


class Answer(DB.Model):
    """Answer model class"""

    __tablename__ = 'answers'

    id = DB.Column(DB.Integer, primary_key=True)
    value = DB.Column(DB.Text, nullable=False, unique=True)

    def __init__(self, value):
        """

        :param value:
        """
        self.value = value

    @staticmethod
    def create(value):
        """

        :param value:
        :return:
        """
        answer = Answer(value)
        DB.session.add(answer)
        DB.session.commit()
        return answer
