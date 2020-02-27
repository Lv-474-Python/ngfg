"""
Form resource API
"""

from flask import request, Response
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden
from flask_login import current_user, login_required

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
        if int(data['owner_id']) != current_user.id:
            raise Forbidden("You cannot create group not for yourself")

        is_correct, errors = GroupService.validate_data(data)
        if not is_correct:
            raise BadRequest(errors)

        group = GroupService.create_group_with_users(
            group_name=data['name'],
            group_owner_id=data['owner_id'],
            emails=data['users_emails']
        )
        if group is None:
            raise BadRequest("Cannot create group")

        return Response(status=201)
