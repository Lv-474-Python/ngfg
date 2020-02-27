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
GROUP_PUT_MODEL = API.inherit('GroupPut', GROUP_MODEL, {
    "emails_add": fields.List(
        cls_or_instance=fields.String,
        required=False,
        description='Group users to add',
        help="List can be empty"),
    "emails_delete": fields.List(
        cls_or_instance=fields.String,
        required=False,
        description='Group users to delete',
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
    Group API

    url: '/groups/'
    methods: get, put, delete
    """
    @API.doc(
        responses={
            200: 'OK',
            400: 'Bad request',
            401: 'Unauthorized',
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self, group_id):
        """
        Get group by id

        :param group_id:
        :return: Group
        """
        group = GroupService.get_by_id(group_id=group_id)
        if group is None:
            raise BadRequest("Group is not found")
        group_json = GroupService.to_json_single(group)
        return jsonify(group_json)

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
            403: 'Forbidden to update group'
        }
    )
    @API.expect(GROUP_PUT_MODEL)
    @login_required
    # pylint: disable=no-self-use
    def put(self, group_id):
        """
        Update single group

        :param group_id:
        :return: 200 if updated
        """
        group = GroupService.get_by_id(group_id=group_id)
        if group is None:
            raise BadRequest("Group is not found")

        if group.owner_id != current_user.id:
            raise BadRequest("You can't update someone else's group")

        group_json = GroupService.to_json(group)
        data = request.get_json()
        group_json.update(**data)

        passed, errors = GroupService.validate_put_data(group_json)
        if not passed:
            return BadRequest(errors)

        updated = GroupService.update_group_name_and_users(
            group_id,
            group_json["emails_add"],
            group_json["emails_delete"],
            group_json["name"])

        if not updated:
            raise BadRequest("Cannot update group")
        return Response(status=200)
