"""
Group service
"""

from app import DB, LOGGER
from app.models import Group
from app.schemas import BaseGroupSchema, GroupPostSchema, GroupPutSchema
from app.services.group_user import GroupUserService
from app.services.user import UserService
from app.helper.decorators import transaction_decorator
from app.helper.errors import (
    GroupNotExist,
    GroupNotCreated,
    UserNotCreated,
    GroupUserNotCreated,
    GroupUserNotDeleted,
    GroupNameAlreadyExist,
    GroupUserAlreadyExist,
    UserNotExist)


class GroupService:
    """
    Class for Group service
    """

    @staticmethod
    @transaction_decorator
    def create(name, owner_id):
        """
        Create Group model

        :param name:
        :param owner_id:
        :return: Group model object or None
        """
        group = Group(name=name, owner_id=owner_id)
        DB.session.add(group)
        return group

    @staticmethod
    @transaction_decorator
    def update(group_id, name=None, owner_id=None):
        """
        Update Group model

        :param group_id:
        :param name:
        :param owner_id:
        :return: updated Group object or None
        """
        group = GroupService.get_by_id(group_id)

        if group is None:
            raise GroupNotExist()

        if name is not None:
            group.name = name
        if owner_id is not None:
            group.owner_id = owner_id

        DB.session.merge(group)
        return group

    @staticmethod
    @transaction_decorator
    def delete(group_id):
        """
        Delete Group model by id

        :param group_id:
        :return: True if model is deleted or None
        """
        group = GroupService.get_by_id(group_id)

        if group is None:
            raise GroupNotExist()

        DB.session.delete(group)
        return True

    @staticmethod
    def get_by_id(group_id):
        """
        Get Group model by id

        :param group_id:
        :return: Group object or None
        """
        group = Group.query.get(group_id)
        return group

    @staticmethod
    def filter(group_id=None, name=None, owner_id=None):
        """
        Group filter method

        :param group_id:
        :param name:
        :param owner_id:
        :return: list of Group objects or empty list
        """
        filter_data = {}

        if group_id is not None:
            filter_data['id'] = group_id
        if name is not None:
            filter_data['name'] = name
        if owner_id is not None:
            filter_data['owner_id'] = owner_id

        result = Group.query.filter_by(**filter_data).all()
        return result

    @staticmethod
    def get_users_by_group(group_id):
        """
        Get all users in group by group_id

        :param group_id:
        :return: list of Users objects or empty list
        """
        group = GroupService.get_by_id(group_id)
        if group is None:
            LOGGER.error('error occured %s', GroupNotExist())
            return None

        users = []

        for group_user in group.groups_users:
            users.append(UserService.to_json(group_user.user))

        return users

    @staticmethod
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = BaseGroupSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def to_json_all(data):
        """
        Get all group objects
        """
        result = GroupService.to_json(data, many=True)

        if not isinstance(result, list):
            result = [result]

        for group in result:
            group['users'] = GroupService.get_users_by_group(group['id'])

        return result

    @staticmethod
    def to_json_single(data):
        """
        Get data in json format
        """
        group = GroupService.to_json(data, many=False)
        group['users'] = GroupService.get_users_by_group(group['id'])

        return group

    @staticmethod
    def validate_post_data(data, user):
        """
        Validate data by GroupPostSchema
        """
        schema = GroupPostSchema()
        errors = schema.validate(data)
        is_exist = GroupService.filter(name=data.get('name'), owner_id=user)
        if is_exist:
            errors['is_exist'] = 'Group with such name already exist'
        return (not bool(errors), errors)

    @staticmethod
    @transaction_decorator
    def create_group_with_users(
            group_name,
            group_owner_id,
            emails):
        """
        Create group
        - create group
        - create users by email
        - assign group users

        :param group_name: group name
        :param group_owner_id: group owner id
        :param emails: list of emails
        :return: created group
        """
        # create group
        group = GroupService.create(group_name, group_owner_id)
        if group is None:
            raise GroupNotCreated()

        # create users by email
        users = UserService.create_users_by_emails(emails)
        if users is None:
            raise UserNotCreated()

        # assign groups_users
        group_users = GroupService.assign_users_to_group(group.id, users)
        if group_users is None:
            raise GroupUserNotCreated()

        return group

    @staticmethod
    @transaction_decorator
    def assign_users_to_group(group_id, users):
        """
        Having group id and list of users create Groups_Users

        :param group_id: group id
        :param users: list of users in group
        :return: list of group users
        """
        group_users = []
        for user in users:
            group_user = GroupUserService.create(group_id, user.id)
            if group_user is None:
                raise GroupUserNotCreated()
            group_users.append(group_user)
        return group_users

    @staticmethod
    def validate_put_data(data, user, group_id):
        """
        Validate data by GroupScheme
        """
        data = data.copy()
        del data['created']
        schema = GroupPutSchema()
        errors = schema.validate(data)
        updated_name = data.get('name')
        if updated_name:
            is_changed = not bool(GroupService.filter(name=updated_name, group_id=group_id))
            if is_changed:
                is_exist = GroupService.filter(owner_id=user, name=updated_name)
                if is_exist:
                    errors['is_exist'] = 'Group with such name already exist'
        return (not bool(errors), errors)

    @staticmethod
    @transaction_decorator
    def update_group_name_and_users(group_id, emails_add, emails_delete, name):
        """
        Method to add or delete users from group and update name

        :param group_id:
        :param emails_add:
        :param emails_delete:
        :param name:
        :return:
        """
        group = GroupService.get_by_id(group_id)
        if group is None:
            raise GroupNotExist()

        is_updated = GroupService.update(group_id, name=name)
        if is_updated is None:
            raise GroupNameAlreadyExist()

        users = UserService.create_users_by_emails(emails_add)
        if users is None:
            raise UserNotCreated()

        group_users = GroupService.assign_users_to_group(group_id, users)
        if group_users is None:
            raise GroupUserNotCreated()
        deleted = GroupService.unsign_users_by_email(
            group_id,
            emails_delete
        )
        if not deleted:
            raise GroupUserNotDeleted()

        return True

    @staticmethod
    @transaction_decorator
    def unsign_users_by_email(group_id, users_emails):
        """
        Delete from group by emails

        :param group_id:
        :param users_emails: list
        :return: True if deleted all
        """
        for user_email in users_emails:
            user = UserService.filter(email=user_email)

            if not user:
                raise UserNotExist()

            user = user[0]
            in_group = bool(GroupUserService.filter(
                group_id=group_id,
                user_id=user.id))

            if not in_group:
                raise GroupUserAlreadyExist()
            GroupUserService.delete_by_group_and_user_id(
                group_id=group_id,
                user_id=user.id)
        return True

    @staticmethod
    def check_whether_groups_exist(groups_ids):
        """
        Check whether groups by given ids exist

        :param groups_ids: ids of groups that will be checked
        """
        errors = []

        for group_id in groups_ids:
            group = GroupService.get_by_id(group_id)
            if group is None:
                errors.append(f"Group {group_id} doesn't exist")

        return errors
