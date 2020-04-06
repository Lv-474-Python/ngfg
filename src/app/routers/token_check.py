"""
Token resource API
"""

from werkzeug.exceptions import BadRequest
from flask import Response
from flask_restx import Resource
from flask_login import current_user

from app import API
from app.services import TokenService, FormResultService


FORM_TOKEN_NS = API.namespace('tokens/<string:token>')


@FORM_TOKEN_NS.route("/check_user")
class TokenUserCheckAPI(Resource):
    """
    TokenUserCheckAPI API

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
                raise BadRequest("You have already passed this form")

        return Response(status=204)
