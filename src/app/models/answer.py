"""Answer model"""
from app import DB
from .abstractModel import AbstractModel


class Answer(AbstractModel):
    """Answer model class"""

    __tablename__ = 'answers'

    value = DB.Column(DB.Text, nullable=False, unique=True)

    def __init__(self, value):
        """

        :param value:
        """
        super().__init__(self)
        self.value = value


