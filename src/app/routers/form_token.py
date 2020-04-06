"""
Token resource API
"""

from werkzeug.exceptions import BadRequest
from flask import Response
from flask_restx import Resource

from app import API
from app.services import FormService, TokenService, GroupService


FORM_TOKEN_NS = API.namespace('forms/<int:form_id>/tokens/')


@FORM_TOKEN_NS.route("/<string:token>/check")
class FormTokenCheckAPI(Resource):
    """
    FormTokenCheckAPI API

    url: '/forms/{form_id}/tokens/{token}/check'
    methods: get
    """

    @API.doc(
        responses={
            204: 'No Content',
            400: 'Invalid data'
        },
        params={
            'form_id': 'id of form',
            'token': 'token to form'
        }
    )
    #pylint: disable=no-self-use
    def get(self, form_id, token):
        """
        Check whether user can answer on form by using this token

        :param token: token to check
        """
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form doesn't exist")

        token_instance = TokenService.get_by_token(token)
        if token_instance is None:
            raise BadRequest("Token doesn't exist")

        if form_id != token_instance.form_id:
            raise BadRequest("Token doesn't match form")

        # form_answer =
        # current_user коли немає то він None чи в нього id None





        # token_instance = TokenService.get_by_token(token)
        # if token_instance is None:
        #     raise BadRequest({'errors': 'Wrong token'})

        # token_data = TokenService.decode_token_for_check(token)
        # if token_data is None:
        #     raise BadRequest({'errors': 'Wrong token'}) # Not enough token segments

        # is_correct, _ = TokenService.validate_data(token_data)
        # if not is_correct:
        #     raise BadRequest({'errors': 'Wrong token'}) # Token isn't valid

        # form_id = token_data.get('form_id')
        # form = FormService.get_by_id(form_id)
        # if form is None:
        #     raise BadRequest({'errors': 'Wrong token'}) # Form doesn't exist

        # group_id = token_data.get('group_id')
        # if group_id is not None:
        #     group = GroupService.get_by_id(group_id)
        #     if group is None:
        #         raise BadRequest({'errors': 'Wrong token'}) # Group doesn't exist

        return Response(status=204)
