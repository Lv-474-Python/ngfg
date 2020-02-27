"""
Group resource API
"""

from flask import jsonify
from flask_restx import Resource
from flask_login import current_user, login_required
from werkzeug.exceptions import Forbidden, BadRequest

from app import API
from app.services import GroupService

GROUP_NS = API.namespace('groups', description='Group APIs')


@GROUP_NS.route("/")
class GroupsAPI(Resource):
    """
        Groups API

        url: '/groups/'
        methods: get
    """

    @API.doc(
        responses={
            401: 'Unauthorized',
            200: 'OK',
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self):
        """
        Get all groups created by user

        """
        groups = GroupService.filter(owner_id=current_user.id)

        groups_json = GroupService.to_json_all(groups)
        return jsonify(groups_json)


@GROUP_NS.route("<int:group_id>")
class GroupAPI(Resource):
    """
    Class
    """

    @login_required
    # pylint: disable=no-self-use
    def get(self, group_id):
        """
        :param group_id:
        :return:
        """
        group = GroupService.get_by_id(group_id=group_id)
        if group is None:
            raise BadRequest("Group is not found")
        group_json = GroupService.to_json(group, many=False)
        return jsonify(group_json)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden to delete'
        }, params={
            'group_id': 'Specify the Id associated with the group'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def delete(self, group_id):
        """
        Delete group

        :param group_id:
        """
        group = GroupService.get_by_id(group_id=group_id)
        if group is None:
            raise BadRequest("Group is not found")

        if group.user != current_user:
            raise Forbidden("Deleting group is forbidden")

        is_deleted = bool(GroupService.delete(group_id))
        if not is_deleted:
            raise BadRequest("Couldn't delete group")

        return jsonify({'is_deleted': is_deleted})
