"""
User resource API
"""

from flask import jsonify
from flask_restx import Resource
from werkzeug.exceptions import BadRequest

from app import API
from app.services import UserService


USER_NS = API.namespace('users', description='User APIs')


@USER_NS.route("/<int:user_id>")
class UserAPI(Resource):
    """
    User API

    url: '/users/{id}'
    methods: get
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax'
        }, params={
            'user_id': 'Specify the Id associated with the user'
        }
    )
    #pylint: disable=no-self-use
    def get(self, user_id):
        """
        Get user by id

        :param user_id: user id
        """
        user = UserService.get_by_id(user_id)
        if user is None:
            raise BadRequest("User with given id wasn't found")

        user_json = UserService.to_json(user)
        return jsonify(user_json)
