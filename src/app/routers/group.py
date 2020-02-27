"""
Group api
"""
from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import login_required
from werkzeug.exceptions import BadRequest

from app import API
from app.services import GroupService, GroupUserService

GROUP_NS = API.namespace('groups', description='Group APIs')

GROUP_MODEL = API.model('Group', {
    "name": fields.String(required=True)
})

GROUP_PUT_MODEL = API.inherit('GroupPut', GROUP_MODEL, {
    "emails_add": fields.List(fields.String),
    "emails_delete": fields.List(fields.String)
})


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

    @login_required
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
