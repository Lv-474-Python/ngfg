"""
Form resource API
"""

from flask import request, jsonify, Response
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden
from flask_login import current_user, login_required

from app import API
from app.services import FormService


FORM_NS = API.namespace('forms', description='Form APIs')
MODEL = API.model('Form', {
    'name': fields.String(
        required=True,
        description="Form name",
        help="Name cannot be blank"),
    'title': fields.String(
        required=True,
        description="Form title",
        help="Title cannot be blank"),
    'resultUrl': fields.Url(
        required=True,
        description="Url where results are stored"),
    'isPublished': fields.Boolean(
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
        return jsonify({"forms": forms_json})

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
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
        is_correct, errors = FormService.validate_post_data(data=data, user=current_user.id)
        if not is_correct:
            raise BadRequest(errors)

        form = FormService.create(
            owner_id=current_user.id,
            name=data['name'],
            title=data['title'],
            result_url=data['resultUrl'],
            is_published=data['isPublished']
        )
        if form is None:
            raise BadRequest("Cannot create form instance")

        form_json = FormService.to_json(form, many=False)
        response = jsonify(form_json)
        response.status_code = 201
        return response


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
            400: 'Invalid data'
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
            400: 'Invalid data',
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
        if form_json.get('ownerId') is not None:
            del form_json['ownerId']
        data = request.get_json()
        form_json.update(data)
        is_correct, errors = FormService.validate_put_data(
            data=form_json,
            user=current_user.id,
            form_id=form_id
        )
        if not is_correct:
            raise BadRequest(errors)

        # update form
        updated_form = FormService.update(
            form_id=form_id,
            name=data.get('name'),
            title=data.get('title'),
            result_url=data.get('resultUrl'),
            is_published=data.get('isPublished')
        )
        if updated_form is None:
            raise BadRequest("Couldn't update form")

        form_json = FormService.to_json(updated_form, many=False)
        return jsonify(form_json)

    @API.doc(
        responses={
            204: 'No content',
            400: 'Invalid data',
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

        is_deleted = FormService.delete(form_id)
        if is_deleted is None:
            raise BadRequest("Couldn't delete form")

        return Response(status=204)
