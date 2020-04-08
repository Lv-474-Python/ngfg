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


FORM_ANSWER_NS = API.namespace('forms/<int:form_id>/answers', description='FormAnswer APIs')
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


@FORM_ANSWER_NS.route("")
class AnswersAPI(Resource):
    """

    url: /forms/{form_id}/answers
    methods: post, get
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Bad request',
            401: 'Unauthorized'
        },
        params={'form_id': 'Specify the form_id'}
    )
    # pylint: disable=no-self-use
    @login_required
    def get(self, form_id):
        """
        Get method for form answers

        :param form_id:
        :return: All answers for form if owner, else answer of current user.
        """
        form = FormService.get_by_id(form_id)
        answers = []
        if form is None:
            raise BadRequest("No such form")
        if form.owner_id == current_user.id:
            token = TokenService.filter(form_id=form.id)[0]
            result = FormResultService.filter(token_id=token.id)
            answers = FormResultService.to_json(result, many=True)
        else:
            token = TokenService.filter(form_id=form.id)[0]
            result = FormResultService.filter(user_id=current_user.id, token_id=token.id)
            if result:
                answers = FormResultService.to_json(result[0], many=False)

        return jsonify({"formAnswers": answers})

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            403: 'Forbidden to create'}
    )
    @API.expect(MODEL)
    # pylint: disable=no-self-use
    def post(self, form_id):
        """
        Creates FormResult

        :param form_id:
        :return: created FormResult with answer id's instead of text answers of user
        """
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

        token = TokenService.filter(form_id=form_id)[0]
        result = FormResultService.create(
            user_id=result['user_id'],
            token_id=token.id,
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


@FORM_ANSWER_NS.route("/<int:result_id>")
class AnswerAPI(Resource):
    """

    url: /forms/{form_id}/answers{answer_id}
    methods: get
    """
    @API.doc(
        responses={
            200: 'OK',
            400: 'Bad request',
            401: 'Unauthorized'
        },
        params={
            'form_id': 'Specify the form_id',
            'result_id': 'Specify the result_id'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self, form_id, result_id):
        """
        Get FormResult by Id

        :param form_id:
        :param result_id:
        :return:
        """
        form = FormService.get_by_id(form_id)
        result = FormResultService.get_by_id(result_id)
        token = TokenService.get_by_id(result.token_id)
        if not (form and result and token):
            raise BadRequest("Result with such parameters is not found.")
        if form.id != token.form_id:
            raise BadRequest("Wrong result to form relation!")
        return FormResultService.to_json(result, many=False)


@TOKEN_ANSWER_NS.route("")
class FormTokenAnswersAPI(Resource):
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

        form = FormService.get_by_id(token_data.get('form_id'))
        if form is None:
            raise BadRequest('Wrong token')

        # validate data
        result = request.get_json()
        result['form_id'] = form.id
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
        result['answers'] = FormResultService.create_answers_dict(form.id, result['answers'])

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

        form_url = FormService.get_form_result_url(form.id)
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
