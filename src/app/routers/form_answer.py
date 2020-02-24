import json

from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import current_user
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
    def get(self, form_id):
        """
        Get method for form answers

        :param form_id:
        :return: All answers for form if owner, else answer of current user.
        """
        if current_user.is_anonymous:
            return jsonify('You are not logged in!')
        form = FormService.get_by_id(form_id)
        answers = []
        if form.owner_id == current_user.id:
            answers = FormResultService.to_json(form.form_results, many=True)
        else:
            result = FormResultService.filter(user_id=current_user.id, form_id=form.id)
            if not result:
                return jsonify("You haven't answered yet!")
            answers = FormResultService.to_json(result[0], many=False)
        return jsonify(answers)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'},)
    @API.expect(MODEL)
    def post(self, form_id):
        """
        Creates FormResult

        :param form_id:
        :return: created FormResult with answer id's instead of text answers of user
        """
        form_result = request.get_json()
        for answer in form_result['answers']:
            ans = AnswerService.create(answer['answer_id'])
            if ans:
                answer['answer_id'] = ans.id
            else:
                answer['answer_id'] = AnswerService.get_by_value(str(answer['answer_id'])).id
        result = FormResultService.create(**form_result)
        return jsonify(result)


@FORM_ANSWER_NS.route("/<int:result_id>")
class AnswerAPI(Resource):

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
    def get(self, form_id, result_id):
        form = FormService.get_by_id(form_id)
        result = FormResultService.get_by_id(result_id)
        if not (form and result):
            return jsonify("not found")
        if form.id != result.form_id:
            return jsonify("wrong result to form relation!")
        return FormResultService.to_json(result, many=False)
