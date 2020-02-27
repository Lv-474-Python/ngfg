"""
Form resource API
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
