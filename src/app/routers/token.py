"""
Token resource API
"""

from werkzeug.exceptions import BadRequest
from flask import request, jsonify, Response
from flask_restx import Resource, fields
from flask_login import current_user

from app import API
from app.services import FormService, TokenService, GroupService


TOKEN_NS = API.namespace('tokens')


@TOKEN_NS.route("/<string:token>/check")
class TokenCheckAPI(Resource):
    """
    Tokens API

    url: '/tokens/{token}/check'
    methods: get
    """

    @API.doc(
        responses={
            204: 'No Content',
            400: 'Invalid data'
        },
        params={
            'token': 'token to check'
        }
    )
    #pylint: disable=no-self-use
    def get(self, token):
        """
        Check whether token is valid

        :param token: token to check
        """

        # чи треба перевіряти чи токен створений нами


        token_data = TokenService.decode_token_for_check(token)
        if token_data is None:
            raise BadRequest({'errors': 'Wrong token'}) # Not enough token segments

        is_correct, _ = TokenService.validate_data(token_data)
        if not is_correct:
            raise BadRequest({'errors': 'Wrong token'}) # Token isn't valid

        form_id = token_data.get('form_id')
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest({'errors': 'Wrong token'}) # Form doesn't exist

        group_id = token_data.get('group_id')
        if group_id is not None:
            group = GroupService.get_by_id(group_id)
            if group is None:
                raise BadRequest({'errors': 'Wrong token'}) # Group doesn't exist

        return Response(status=204)
