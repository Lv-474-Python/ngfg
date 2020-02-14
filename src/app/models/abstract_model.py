"""abstract model"""
from sqlalchemy.exc import IntegrityError

from app import DB


class AbstractModel(DB.Model):
    """abstract model class"""

    __abstract__ = True

    id = DB.Column(DB.Integer, primary_key=True)

    @classmethod
    def create(cls, **kwargs):
        """

        :param value:
        :return:
        """
        instance = cls(**kwargs)
        try:
            DB.session.add(instance)
            DB.session.commit()
        except IntegrityError:
            return None
        return instance

    @classmethod
    def get_by_id(cls, pk):  # pylint: disable=invalid-name
        """get by id"""

    @classmethod
    def update(cls, **kwargs):
        """update"""

    @classmethod
    def delete_by_id(cls, pk):  # pylint: disable=invalid-name
        """delete by id"""
