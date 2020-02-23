"""
Form resource API
"""

from flask import request, jsonify
from flask_restx import Resource, fields
from flask_login import current_user

from app import API
from app.services import FormService
from app.helper.errors import (
    NotFound, BadRequest, Forbidden
)


NS = API.namespace('forms', description='Form APIs')
MODEL = API.model('Form', {
    'owner_id': fields.Integer(
        required=True,
        description="Owner id",
        help="Owner id cannot be blank"),
    'name': fields.String(
        required=True,
        description="Form name",
        help="Name cannot be blank"),
    'title': fields.String(
        required=True,
        description="Form title",
        help="Title cannot be blank"),
    'result_url': fields.Url(
        required=True,
        description="Url where results are stored"),
    'is_published': fields.Boolean(
        required=True,
        description="If form is published")})


@NS.route("/")
class FormsAPI(Resource):
    """
    Forms API

    url: '/forms/'
    methods: get, post
    """

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
            404: 'Forms not found'
        }
    )
    # pylint: disable=no-self-use
    def get(self):
        """
        Get all forms created by requested user
        """
        forms = FormService.filter(owner_id=current_user.id)
        if not forms:
            raise NotFound("You didn't create any form yet")

        forms_json = FormService.to_json(forms, many=True)
        response = {"forms": forms_json}
        return jsonify(response)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized'
        }
    )
    @API.expect(MODEL)
    # pylint: disable=no-self-use
    def post(self):
        """
        Create new form
        """
        data = request.get_json()
        form = FormService.create(**data)
        if form is None:
            raise BadRequest("Cannot create form instance")

        form_json = FormService.to_json(form, many=False)
        return jsonify(form_json)


@NS.route("/<int:id>")
class FormAPI(Resource):
    """
    Form API

    url: '/forms/{id}'
    methods: get, put, delete
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid ID',
            404: 'Form not found'},
        params={
            'id': 'Specify the Id associated with the form'}
    )
    #pylint: disable=no-self-use
    def get(self, id):  # pylint: disable=redefined-builtin
        """
        Get form by id

        :param id: form id
        """
        form = FormService.get_by_id(id)
        if form is None:
            raise NotFound("Form with given id wasn't found")

        form_json = FormService.to_json(form, many=False)
        return jsonify(form_json)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden to update',
            404: 'Form not found'},
        params={
            'id': 'Specify the Id associated with the form'}
    )
    @API.expect(MODEL, validate=False)
    # pylint: disable=no-self-use
    def put(self, id):  # pylint: disable=redefined-builtin
        """
        Update form

        :param id: form id
        """

        form = FormService.get_by_id(id)
        if form is None:
            raise NotFound("Form with given id wasn't found")
        if form.owner != current_user:
            raise Forbidden("Updating form with is forbidden")

        data = request.get_json()
        updated_form = FormService.update(form.id, **data)
        if updated_form is None:
            raise BadRequest("Couldn't update form")

        form_json = FormService.to_json(updated_form, many=False)
        return jsonify(form_json)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax', # if string id for example. Swagger handle it
            401: 'Unauthorized',
            403: 'Forbidden to delete',
            404: 'Form not found'},
        params={
            'id': 'Specify the Id associated with the form'}
    )
    # pylint: disable=no-self-use
    def delete(self, id):  # pylint: disable=redefined-builtin
        """
        Delete form

        :param id: form id
        """

        form = FormService.get_by_id(id)
        if form is None:
            raise NotFound("Form with given id wasn't found")
        if form.owner != current_user:
            raise Forbidden("Deleting form is forbidden")

        is_deleted = bool(FormService.delete(id))
        if not is_deleted:
            raise BadRequest("Couldn't delete form")

        return jsonify({'is_deleted': is_deleted})
