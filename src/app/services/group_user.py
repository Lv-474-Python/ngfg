"""
A service to handle GroupUser operations
"""

from app import DB
from app.models import GroupUser
from app.helper.decorators import transaction_decorator
from app.helper.errors import GroupUserNotExist
from app.services.user import UserService


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

    @staticmethod
    def delete_users_by_email(group_id, users_emails):
        """

        :param group_id:
        :param users_emails:
        :return:
        """
        errors = {}
        for user_email in users_emails:
            user = UserService.filter(email=user_email)
            if not user:
                errors[user_email] = "No such user"
                return False, errors
            user = user[0]
            in_group = bool(GroupUserService.filter(
                group_id=group_id,
                user_id=user.id))
            if not in_group:
                errors[user_email] = "No such user in this group"
                return False, errors
            if not GroupUserService.delete_by_group_and_user_id(
                    group_id=group_id,
                    user_id=user.id):
                errors[user_email] = "Failed to delete from group"
                return False, errors
        return (not bool(errors), errors)

    @staticmethod
    def add_users_by_email(group_id, users_emails):
        """

        :param group_id:
        :param users_emails:
        :return:
        """
        errors = {}
        for user_email in users_emails:
            user = UserService.create_user_by_email(user_email)
            in_group = bool(GroupUserService.filter(
                group_id=group_id,
                user_id=user.id))
            if in_group:
                errors[user_email] = "User is already in this group"
                return False, errors
            group_user = GroupUserService.create(
                group_id=group_id,
                user_id=user.id)
            if group_user is None:
                errors[user_email] = "Failed to add in group"
                return False, errors
        return (not bool(errors), errors)
