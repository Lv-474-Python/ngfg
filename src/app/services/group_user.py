"""
A service to handle GroupUser operations
"""

from app import DB
from app.models import GroupUser
from app.helper.decorators import transaction_decorator
from app.helper.errors import GroupUserNotExist


class GroupUserService:
    """
    GroupUser service class
    """

    @staticmethod
    @transaction_decorator
    def create(group_id, user_id):
        """
        GroupUser model create method

        :param group_id:
        :param user_id:
        :return: created GroupUser object or None
        """
        group_user = GroupUser(group_id=group_id, user_id=user_id)
        DB.session.add(group_user)
        return group_user

    @staticmethod
    @transaction_decorator
    def delete_by_group_and_user_id(group_id, user_id):
        """
        GroupUser model delete method

        :param group_id:
        :param user_id:
        :return: True if object was deleted or None
        """
        group_user = GroupUserService.get_by_group_and_user_id(group_id, user_id)
        if group_user is None:
            raise GroupUserNotExist()

        DB.session.delete(group_user)
        return True

    @staticmethod
    def filter(user_id=None, group_id=None):
        """
        GroupUser model filter method

        :param user_id:
        :param group_id:
        :return: list of GroupUser objects or empty list
        """
        filter_data = {}

        if user_id is not None:
            filter_data['user_id'] = user_id
        if group_id is not None:
            filter_data['group_id'] = group_id

        result = GroupUser.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    def get_by_group_and_user_id(group_id, user_id):
        """
        GroupUser model get by group_id and user_id

        :param group_id:
        :param user_id:
        :return: GroupUser object or None
        """
        group_user_list = GroupUserService.filter(user_id, group_id)
        if group_user_list:
            return group_user_list[0]

        raise GroupUserNotExist()
