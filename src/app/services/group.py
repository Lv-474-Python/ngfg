"""
Group service
"""

from app.models import Group, BaseGroupSchema, GroupPutSchema
from app import DB
from app.helper.decorators import transaction_decorator
from app.helper.errors import GroupNotExist
from app.services import UserService


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
            raise GroupNotExist()

        users = []

        for group_user in group.groups_users:
            users.append(UserService.to_json(group_user.user))

        return users

    # @staticmethod
    # def to_json(data, many=False):

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
    def validate_data(data):
        """
        Validate data by GroupScheme
        """
        schema = BaseGroupSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)

    @staticmethod
    def validate_put_data(data):
        """
        Validate data by GroupScheme
        """
        schema = GroupPutSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)
