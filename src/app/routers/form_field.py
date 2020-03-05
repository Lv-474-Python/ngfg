"""
FormField resource API
"""

from flask import request, jsonify, Response
from flask_login import current_user, login_required
from flask_restx import Resource, fields
from werkzeug.exceptions import BadRequest, Forbidden

from app import API
from app.services import (FormFieldService, FormService, SharedFieldService, FieldService)

FORM_FIELD_NS = API.namespace('forms/<int:form_id>/fields', description='FormField APIs')
FORM_FIELD_MODEL = API.model('FormField', {
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


@FORM_FIELD_NS.route('/')
class FormFieldsAPI(Resource):
    """
    FormFields API

    url: 'forms/{form_id}/fields/'
    methods: get, post
    """

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
        },
        params={
            'form_id': 'Specify ID of the form to view its fields'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self, form_id):
        """
        Get all fields that are contained within a form

        :param form_id: ID of the form that contains fields
        """

        form = FormService.get_by_id(form_id=form_id)
        if form is None:
            raise BadRequest("No such form")
        if form.owner_id != current_user.id:
            raise Forbidden("Can't view fields of the form that doesn't belong to you")

        form_fields = FormFieldService.filter(form_id=form.id)
        return jsonify(FormFieldService.to_json(form_fields, many=True))

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden creation'
        },
        params={
            'form_id': 'Specify ID of the form you want to insert fields into',
        }
    )
    @API.expect(FORM_FIELD_MODEL)
    @login_required
    # pylint: disable=no-self-use
    def post(self, form_id):
        """
        Add field to a form

        :param form_id: ID of the form to which the field will be inserted
        """

        form = FormService.get_by_id(form_id)

        if form is None:
            raise BadRequest("No such form")
        if form.owner_id != current_user.id:
            raise Forbidden("Can't insert fields into the form that doesn't belong to you")

        data = request.get_json()
        field = FieldService.get_by_id(int(data['field_id']))
        shared_fields = [fld.field_id for fld in SharedFieldService.filter(user_id=current_user.id)]

        if field is None:
            raise BadRequest("Can't add nonexistent field to form")
        if field.owner_id != current_user.id and field.id not in shared_fields:
            raise Forbidden("You don't have permission to add this field to your form")
        is_correct, errors = FormFieldService.validate_data(data)
        if not is_correct:
            raise BadRequest(errors)

        form_field = FormFieldService.create(form_id=form_id, **data)
        if form_field is None:
            raise BadRequest("Couldn't create field")
        field_json = FieldService.field_to_json(field, many=False)
        field_json.update(FieldService.get_additional_options(
                                                            field_id=field.id,
                                                            field_type=field.field_type)
                                                                )
        form_field_json = FormFieldService.response_to_json(form_field, many=False)
        form_field_json["field"] = field_json
        response = jsonify(form_field_json)
        response.status_code = 201
        return response


@FORM_FIELD_NS.route('/<int:form_field_id>')
class FormFieldAPI(Resource):
    """
    FormField api

    url: '/forms/{form_id}/fields/{form_field_id}'
    methods: get, put, delete
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid FormField ID',
        },
        params={
            'form_id': 'Specify ID of the form that contains the field you want to view',
            'form_field_id': 'Specify ID of the field you want to view'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def get(self, form_id, form_field_id):
        """
        Get field from a form

        :param form_id: ID of the form
        :param form_field_id: ID of the field contained within a form
        """

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("No such form")
        form_field = FormFieldService.get_by_id(form_field_id)
        if form_field is None:
            raise BadRequest("There's no field with this ID")
        if form_field.form_id != form.id:
            raise BadRequest("This field does not belong to the form you specified")
        return jsonify(FormFieldService.to_json(form_field))

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden update',
        },
        params={
            'form_id': 'ID of the form that contains the field you want to update',
            'form_field_id': 'ID of the field you want to update'
        }
    )
    @API.expect(FORM_FIELD_MODEL, validate=False)
    @login_required
    # pylint: disable=no-self-use
    def put(self, form_id, form_field_id):
        """
        Update field within a form

        :param form_id: ID of the form
        :param form_field_id: ID of the field contained within a form
        """

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("No such form")
        if form.owner_id != current_user.id:
            raise Forbidden("You can't update fields in this form")
        form_field = FormFieldService.get_by_id(form_field_id)
        if form_field is None:
            raise BadRequest("No such field")
        if form_field.form_id != form.id:
            raise BadRequest("The field with such id doesn't belong in this form")

        form_field_json = FormFieldService.to_json(form_field)
        data = request.get_json()
        form_field_json.update(**data)
        is_correct, errors = FormFieldService.validate_data(form_field_json)
        if not is_correct:
            raise BadRequest(errors)

        updated_form_field = FormFieldService.update(form_field_id=form_field_id, **data)
        if updated_form_field is None:
            raise BadRequest("Couldn't update field")

        return Response(status=200)

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden deletion',
        },
        params={
            'form_id': 'ID of the form from which you want the field removed',
            'form_field_id': 'ID of the field you want to delete'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def delete(self, form_id, form_field_id):
        """
        Remove field from a form

        :param form_id: ID of the form
        :param form_field_id: ID of the field contained within a form
        """
        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("No such form")
        if form.owner_id != current_user.id:
            raise Forbidden("Can't delete fields from form you didn't create")
        form_field = FormFieldService.get_by_id(form_field_id)
        if form_field is None:
            raise BadRequest("No such field")
        if form_field.form_id != form.id:
            raise BadRequest("No such field in this form")

        is_deleted = bool(FormFieldService.delete(form_field_id))
        if not is_deleted:
            raise BadRequest("Failed to delete field")
        return Response(status=200)
