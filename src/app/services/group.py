"""
Group service
"""


from app import DB
from app.models import Group, GroupSchema
from app.services.group_user import GroupUserService
from app.services.user import UserService
from app.helper.decorators import transaction_decorator
from app.helper.errors import GroupNotExist


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
    def to_json(data, many=False):
        """
        Get data in json format
        """
        schema = GroupSchema(many=many)
        return schema.dump(data)

    @staticmethod
    def validate_data(data):
        """
        Validate data by GroupSchema
        """
        schema = GroupSchema()
        errors = schema.validate(data)
        return (not bool(errors), errors)

    @staticmethod
    @transaction_decorator
    def create_users_by_emails(emails):
        """
        Having list of emails create users

        :param emails: list of emails
        :return: list of users
        """
        users = []
        for email in emails:
            user = UserService.create_user_by_email(email)
            users.append(user)
        return users

    @staticmethod
    @transaction_decorator
    def create_group_users(group_id, users):
        """
        Having group id and list of users create Groups_Users

        :param group_id: group id
        :param users: list of users in group
        :return: list of group users
        """
        group_users = []
        for user in users:
            group_user = GroupUserService.create(group_id, user.id)
            group_users.append(group_user)
        return group_users
