"""
Group resource API
"""

from flask import jsonify
from flask_restx import Resource
from flask_login import current_user, login_required

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

        groups_json = GroupService.to_json(groups, many=True)
        return jsonify(groups_json)
