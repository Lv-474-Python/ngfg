"""
Group resource API
"""

from flask import request, jsonify, Response
from flask_restx import Resource, fields
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden

from app import API
from app.services import GroupService


GROUP_NS = API.namespace('groups', description='Group APIs')
GROUP_MODEL = API.model('Group', {
    'name': fields.String(
        required=True,
        description="Group name"),
})
GROUP_POST_MODEL = API.inherit('GroupPost', GROUP_MODEL, {
    'owner_id': fields.Integer(
        required=True,
        description="Owner id"),
    'users_emails': fields.List(
        cls_or_instance=fields.String,
        required=False,
        description='Group users',
        help="List can be empty")
})


@GROUP_NS.route("/")
class GroupsAPI(Resource):
    """
    Groups API

    url: '/groups/'
    methods: get, post
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

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
            403: 'Forbidden to create group'
        }
    )
    @API.expect(GROUP_POST_MODEL)
    @login_required
    # pylint: disable=no-self-use
    def post(self):
        """
        Create new group
        """
        data = request.get_json()
        is_correct, errors = GroupService.validate_post_data(data)
        if not is_correct:
            raise BadRequest(errors)

        if int(data['owner_id']) != current_user.id:
            raise Forbidden("You cannot create group not for yourself")

        group = GroupService.create_group_with_users(
            group_name=data['name'],
            group_owner_id=data['owner_id'],
            emails=data['users_emails']
        )
        if group is None:
            raise BadRequest("Cannot create group")

        return Response(status=201)


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

        return Response(status=200)
