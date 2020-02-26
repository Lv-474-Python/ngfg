from flask import request, jsonify
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden
from flask_login import current_user, login_required

from app import API
from app.services import GroupService

GROUP_NS = API.namespace('groups', description='Group APIs')


@GROUP_NS.route("/")
class GroupsAPI(Resource):

    @login_required
    def get(self):
        groups = GroupService.filter(owner_id=current_user.id)

        groups_json = GroupService.to_json(groups, many=True)
        response = {"groups": groups_json}
        return jsonify(response)

