"""
Form resource API
"""

from flask import request, jsonify
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden
from flask_login import current_user, login_required

from app import API
from app.services import GroupService


GROUP_NS = API.namespace('groups', description='Group APIs')
GROUP_MODEL = API.model('Group', {
    'owner_id': fields.Integer(
        required=True,
        description="Owner id"),
    'name': fields.String(
        required=True,
        description="Group name"),
})
GROUP_POST_MODEL = API.inherit('GroupPost', GROUP_MODEL, {
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
            200: 'OK',
            400: 'Invalid syntax',
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

        # validate data
        is_correct, errors = GroupService.validate_data(data)
        if not is_correct:
            raise BadRequest(errors)

        # create group
        group = GroupService.create(data['name'], data['owner_id'])
        if group is None:
            raise BadRequest("Cannot create group")

        # create users by email
        emails = data['users_emails']
        users = GroupService.create_users_by_emails(emails)
        if users is None:
            raise BadRequest("Cannot create users")

        # create groups_users
        group_users = GroupService.create_group_users(group.id, users)
        if group_users is None:
            raise BadRequest("Cannot create group users")

        # return json response
        group_json = GroupService.to_json(group, many=False)
        group_json['users_emails'] = emails
        return jsonify(group_json)
