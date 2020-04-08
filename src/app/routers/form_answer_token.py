"""
Form answers API
"""

from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest

from app import API
from app.services import FormService, FormResultService, TokenService
from app.helper.sheet_manager import SheetManager


TOKEN_ANSWER_NS = API.namespace('tokens/<string:token>/answers', description='FormAnswerToken APIs')

ANSWER_MODEL = API.model('Answer', {
    'position': fields.Integer(
        required=True
    ),
    'answer': fields.String(
        required=True
    ),
})

MODEL = API.model('FormResult', {
    'answers': fields.List(
        cls_or_instance=fields.Nested(ANSWER_MODEL),
        required=True,
        description="answers list",
        help="JSON list of dicts {position:int, answer:text}"
    )})


@TOKEN_ANSWER_NS.route("")
class AnswersAPI(Resource):
    """

    url: /tokens/{token}/answers
    methods: post
    """

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            403: 'Forbidden to create'}
    )
    @API.expect(MODEL)
    # pylint: disable=no-self-use
    def post(self, token):
        """
        Creates FormResult

        :param token:
        :return: created FormResult with answer id's instead of text answers of user
        """
        # validate token
        token_instance = TokenService.get_by_token(token)
        if token_instance is None:
            raise BadRequest('Wrong token')

        token_data = TokenService.decode_token_for_check(token)
        if token_data is None:
            raise BadRequest('Wrong token')

        form_id = token_data.get('form_id')
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest('Wrong token')

        # validate data
        result = request.get_json()
        result['form_id'] = form_id
        passed, errors = FormResultService.validate_schema(result)
        if not passed:
            raise BadRequest(errors)
        passed, errors = FormResultService.validate_data(form_result=result)
        if not passed:
            raise BadRequest(errors)

        if not current_user.is_anonymous:
            result['user_id'] = current_user.id
        else:
            result['user_id'] = None
        result['answers'] = FormResultService.create_answers_dict(form_id, result['answers'])

        values = []
        for answer in result['answers'].values():
            values.append(answer)
        values.append(token)

        # save result in db and sheet
        result = FormResultService.create(
            user_id=result['user_id'],
            token_id=token_instance.id,
            answers=result['answers']
        )
        if result is None:
            raise BadRequest("Cannot create result instance")

        form_url = FormService.get_form_result_url(form_id)
        if form_url is None:
            raise BadRequest("Cannot create result instance")

        sheet_id = SheetManager.get_sheet_id_from_url(form_url)
        if sheet_id is None:
            raise BadRequest("Cannot create result instance")

        is_added = SheetManager.append_data(sheet_id, values)
        if is_added is None:
            raise BadRequest("Cannot create result instance")

        result_json = FormResultService.to_json(result, many=False)

        response = jsonify(result_json)
        response.status_code = 201
        return response
