"""
Form answers API
"""

from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import current_user
from werkzeug.exceptions import BadRequest, Forbidden

from app import API
from app.services import FormService, FormResultService, AnswerService

FORM_ANSWER_NS = API.namespace('forms/<int:form_id>/answers', description='NgFg APIs')

MODEL = API.model('FormResult', {
    'user_id': fields.Integer(
        required=True,
        description="User id"),
    'form_id': fields.Integer(
        required=True,
        description="Form id"),
    'created': fields.DateTime(
        required=False,
        description="Created"),
    'answers': fields.List(
        cls_or_instance=fields.String,
        required=True,
        description="answers list",
        help="JSON list of dicts {position:int, answer_id:text"
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
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params={'form_id': 'Specify the form_id'})
    # pylint: disable=no-self-use
    def get(self, form_id):
        """
        Get method for form answers

        :param form_id:
        :return: All answers for form if owner, else answer of current user.
        """
        if current_user.is_anonymous:
            raise Forbidden('You are not logged in!')
        form = FormService.get_by_id(form_id)
        answers = []
        if form.owner_id == current_user.id:
            answers = FormResultService.to_json(form.form_results, many=True)
        else:
            result = FormResultService.filter(user_id=current_user.id, form_id=form.id)
            if result:
                answers = FormResultService.to_json(result[0], many=False)

        return jsonify(answers)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'},)
    @API.expect(MODEL)
    # pylint: disable=no-self-use
    def post(self, form_id):
        """
        Creates FormResult

        :param form_id:
        :return: created FormResult with answer id's instead of text answers of user
        """
        result = request.get_json()
        if result["form_id"] != form_id or result["user_id"] != current_user.id:
            raise BadRequest("Wrong form or/and user id's were passed ")
        #if not FormResultService.validate_answers_positions(result):
        #    raise BadRequest("Wrong positions have been passed")
        passed, errors = FormResultService.validate_data(form_result=result)
        if not passed:
            raise BadRequest(str(errors))
        for answer in result['answers']:
            ans = AnswerService.create(answer['answer'])
            if ans:
                answer['answer_id'] = ans.id
            else:
                answer['answer_id'] = AnswerService.get_by_value(str(answer['answer'])).id
            del answer['answer']
        result = FormResultService.create(**result)
        if result is None:
            raise BadRequest("Cannot create result instance")
        return jsonify(FormResultService.to_json(result))


@FORM_ANSWER_NS.route("/<int:result_id>")
class AnswerAPI(Resource):
    """

    url: /forms/{form_id}/answers{answer_id}
    methods: get
    """
    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params={
            'form_id': 'Specify the form_id',
            'result_id': 'Specify the result_id'
        })
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
