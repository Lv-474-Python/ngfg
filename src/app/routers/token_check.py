"""
TokenCheck API
"""

from werkzeug.exceptions import BadRequest
from flask import Response
from flask_restx import Resource
from flask_login import current_user

from app import API
from app.services import (
    FormService,
    TokenService,
    GroupService,
    FormResultService
)


TOKEN_CHECK_NS = API.namespace('tokens/<string:token>', description='TokenCheck APIs')


@TOKEN_CHECK_NS.route("/check_token")
class TokenCheckAPI(Resource):
    """
    TokenCheck API

    url: '/tokens/{token}/check_token'
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
        token_instance = TokenService.get_by_token(token)
        if token_instance is None:
            raise BadRequest('Wrong token')

        token_data = TokenService.decode_token_for_check(token)
        if token_data is None:
            raise BadRequest('Wrong token') # Not enough token segments

        is_correct, _ = TokenService.validate_data(token_data)
        if not is_correct:
            raise BadRequest('Wrong token') # Token isn't valid

        form_id = token_data.get('form_id')
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest('Wrong token') # Form doesn't exist

        group_id = token_data.get('group_id')
        if group_id is not None:
            group = GroupService.get_by_id(group_id)
            if group is None:
                raise BadRequest('Wrong token') # Group doesn't exist

        return Response(status=204)


@TOKEN_CHECK_NS.route("/check_user")
class TokenUserCheckAPI(Resource):
    """
    TokenUserCheck API

    url: '/tokens/{token}/check_user'
    methods: get
    """

    @API.doc(
        responses={
            204: 'No Content',
            400: 'Invalid data'
        },
        params={
            'token': 'token to form'
        }
    )
    #pylint: disable=no-self-use
    def get(self, token):
        """
        Check whether user can answer to form by using this token
        :param token: token to check
        """
        token_instance = TokenService.get_by_token(token)
        if token_instance is None:
            raise BadRequest("Token doesn't exist")

        if current_user.is_authenticated:
            user_can_answer = FormResultService.check_whether_user_passed_form(
                user_id=current_user.id,
                token_id=token_instance.id,
            )
            if not user_can_answer:
                raise BadRequest("You have already passed this form using this token")

        return Response(status=204)
