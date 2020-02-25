"""
Form resource API
"""

from flask import request, jsonify
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden
from flask_login import current_user, login_required

from app import API
from app.services import FormService


FORM_NS = API.namespace('forms', description='Form APIs')
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


@FORM_NS.route("/")
class FormsAPI(Resource):
    """
    Forms API

    url: '/forms/'
    methods: get, post
    """

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self):
        """
        Get all forms created by requested user
        """
        forms = FormService.filter(owner_id=current_user.id)

        forms_json = FormService.to_json(forms, many=True)
        response = {"forms": forms_json}
        return jsonify(response)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden to create'
        }
    )
    @API.expect(MODEL)
    @login_required
    # pylint: disable=no-self-use
    def post(self):
        """
        Create new form
        """
        data = request.get_json()
        is_correct, errors = FormService.validate_data(data)
        if not is_correct:
            raise BadRequest(errors)
        if int(data['owner_id']) != current_user.id:
            raise Forbidden("Create form is forbidden")

        form = FormService.create(**data)
        if form is None:
            raise BadRequest("Cannot create form instance")

        form_json = FormService.to_json(form, many=False)
        return jsonify(form_json)


@FORM_NS.route("/<int:form_id>")
class FormAPI(Resource):
    """
    Form API

    url: '/forms/{id}'
    methods: get, put, delete
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid ID'
        }, params={
            'form_id': 'Specify the Id associated with the form'
        }
    )
    #pylint: disable=no-self-use
    def get(self, form_id):
        """
        Get form by id

        :param form_id: form id
        """
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form with given id wasn't found")

        form_json = FormService.to_json(form, many=False)
        return jsonify(form_json)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden to update'
        }, params={
            'form_id': 'Specify the Id associated with the form'
        }
    )
    @API.expect(MODEL, validate=False)
    @login_required
    # pylint: disable=no-self-use
    def put(self, form_id):
        """
        Update form

        :param form_id: form id
        """
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form with given id wasn't found")
        if form.owner != current_user:
            raise Forbidden("Updating form is forbidden")

        # validate request body
        form_json = FormService.to_json(form)
        data = request.get_json()
        form_json.update(data)
        is_correct, errors = FormService.validate_data(form_json)
        if not is_correct:
            raise BadRequest(errors)

        # update form
        updated_form = FormService.update(form_id, **data)
        if updated_form is None:
            raise BadRequest("Couldn't update form")

        form_json = FormService.to_json(updated_form, many=False)
        return jsonify(form_json)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden to delete'
        }, params={
            'form_id': 'Specify the Id associated with the form'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def delete(self, form_id):
        """
        Delete form

        :param form_id: form id
        """
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form with given id wasn't found")
        if form.owner != current_user:
            raise Forbidden("Deleting form is forbidden")

        is_deleted = bool(FormService.delete(form_id))
        if not is_deleted:
            raise BadRequest("Couldn't delete form")

        return jsonify({'is_deleted': is_deleted})
