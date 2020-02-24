"""
FormField resource API
"""

from flask import request, jsonify
from flask_login import current_user
from flask_restx import Resource, fields

from app import API
from app.services import FormFieldService, FormService, UserService

name_space = API.namespace('forms/<int:form_id>/fields', description='FormField APIs')
Model = API.model('FormField', {
    'field_id': fields.Integer(
        required=True,
        description="Field id",
        help="Field id can not be blank"),
    'question': fields.String(
        required=True,
        description="Question to the field",
        help="Question can not be blank"),
    'position': fields.Integer(
        required=True,
        description="Position of the field in form")})


@name_space.route('/')
class FormFieldsAPI(Resource):
    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
            500: 'FormField not found'
        },
        params={
            'form_id': 'Id of the form that contains fields'
        }
    )
    def get(self, form_id):
        form = FormService.get_by_id(form_id=form_id)
        if form is None:
            return "Seems like your form doesn't exist yet"
        if form.owner_id != current_user.id:
            return "Hey, you didn't create this form"
        form_fields = FormFieldService.filter(form_id=form.id)
        response = {"form_fields": FormFieldService.convert_to_json(form_fields, True)}
        return response

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized'
        },
        params={
            'form_id': 'Specify id of the form you want to insert fields into',
        }
    )
    @API.expect(Model)
    def post(self, form_id):
        form = FormService.get_by_id(form_id)
        if form is None:
            return "Seems like you're trying to add a field to a form that doesn't exist"
        field_id = request.get_json()['field_id']
        question = request.get_json()['question']
        position = request.get_json()['position']
        form_field = FormFieldService.create(form_id=form_id, field_id=field_id, question=question, position=position)
        return jsonify(FormFieldService.convert_to_json(form_field, False))


@name_space.route('/<int:field_id>')
class FormFieldAPI(Resource):
    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid ID',
            404: 'FormField not found'
        },
        params={
            'form_id': 'Specify id of the form that contains the field',
            'field_id': 'Specify the id of the field'
        }
    )
    def get(self, form_id, field_id):
        pass