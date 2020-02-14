from sqlalchemy.exc import IntegrityError

from app import DB


class AbstractModel(DB.model):
    __abstract__ = True
    id = DB.column(DB.Integer, primary_key=True)

    def __init__(self):
        """

        :param value:
        """

    @classmethod
    def create(cls, **kwargs):
        """

        :param value:
        :return:
        """
        instance = cls(kwargs)
        try:
            DB.session.add(instance)
            DB.session.commit()
        except IntegrityError:
            return None
        return instance

    @classmethod
    def get_by_id(cls, id):
        """get by id"""

    @classmethod
    def update(cls, **kwargs):
        """update"""

    @classmethod
    def delete_by_id(cls, id):
        """delete by id"""

    @classmethod
    def get_by_id(cls, id):
        """get by id"""

