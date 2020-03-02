"""
Form answers API
"""

from flask import request, jsonify, Response
from flask_restx import Resource, fields
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest

from app import API
from app.services import FormService, FormResultService

FORM_ANSWER_NS = API.namespace('forms/<int:form_id>/answers', description='FormAnswer APIs')

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
            answers = FormResultService.to_json(form.form_results, many=True)
        else:
            result = FormResultService.filter(user_id=current_user.id, form_id=form.id)
            if result:
                answers = FormResultService.to_json(result[0], many=False)

        return jsonify(answers)

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
            403: 'Forbidden to create'}
    )
    @API.expect(MODEL)
    @login_required
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
        result['user_id'] = current_user.id
        result['answers'] = FormResultService.create_answers_dict(form_id, result['answers'])
        result = FormResultService.create(**result)
        if result is None:
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
        if not (form and result):
            raise BadRequest("Result with such parameters is not found.")
        if form.id != result.form_id:
            raise BadRequest("Wrong result to form relation!")
        return FormResultService.to_json(result, many=False)
