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
    'usersEmails': fields.List(
        cls_or_instance=fields.String,
        required=False,
        description='Group users',
        help="List can be empty")
})
GROUP_PUT_MODEL = API.inherit('GroupPut', GROUP_MODEL, {
    "emailsAdd": fields.List(
        cls_or_instance=fields.String,
        required=False,
        description='Group users to add',
        help="List can be empty"),
    "emailsDelete": fields.List(
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

        group = GroupService.create_group_with_users(
            group_name=data['name'],
            group_owner_id=current_user.id,
            emails=data['usersEmails']
        )
        if group is None:
            raise BadRequest("Cannot create group")

        group_json = GroupService.to_json(group, many=False)
        group_json["usersEmails"] = data["usersEmails"]
        response = jsonify(group_json)
        response.status_code = 201
        return response


@GROUP_NS.route("/<int:group_id>")
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
            200: 'OK',
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
            raise BadRequest(errors)

        updated = GroupService.update_group_name_and_users(
            group_id,
            group_json["emailsAdd"],
            group_json["emailsDelete"],
            group_json["name"])

        if not updated:
            raise BadRequest("Cannot update group")

        group = GroupService.get_by_id(group_id=group_id)
        group_json = GroupService.to_json_single(group)
        response = jsonify(group_json)
        response.status_code = 200
        return response

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid data',
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
