"""
Group resource API
"""

from flask import request, jsonify, Response
from flask_restx import Resource, fields
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden

from app import API
from app.services import GroupService, GroupUserService


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
    "emails_add": fields.List(fields.String),
    "emails_delete": fields.List(fields.String)
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

    @API.expect(GROUP_PUT_MODEL)
    @login_required
    # pylint: disable=no-self-use
    def put(self, group_id):
        """

        :param group_id:
        :return:
        """
        data = request.get_json()
        group = GroupService.get_by_id(group_id=group_id)
        passed, errors = GroupService.validate_put_data(data)
        if not passed:
            return jsonify(errors)
        if group is None:  # need transactions to all these checks
            raise BadRequest("Group is not found")
        is_updated = GroupService.update(group_id, name=data["name"])
        if is_updated is None:
            raise BadRequest("Couldn't update group name")
        passed, errors = GroupUserService.delete_users_by_email(
            group_id,
            data["emails_delete"]
        )
        if not passed:
            return jsonify(errors)
        passed, errors = GroupUserService.add_users_by_email(
            group_id,
            data["emails_add"]
        )
        if not passed:
            return jsonify(errors)
        #form_json = GroupService.to_json(updated_form, many=False)
        return jsonify("form_json")
