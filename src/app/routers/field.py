"""
Field router.
"""
from flask import request, jsonify, Response
from flask_restx import fields, Resource
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden
from app.models import FieldPutSchema

from app import API
from app.helper.enums import FieldType
from app.services import FieldService

FIELDS_NS = API.namespace('fields', description='NgFg APIs')

FIELD_MODEL = API.model('Field', {
    'name': fields.String(required=True),
    'owner_id': fields.Integer(required=True),
    'field_type': fields.Integer(required=True)
})
AUTOCOMPLETE_MODEL = API.model('Setting_autocomplete', {
    "data_url": fields.Url,
    "sheet": fields.String,
    "from_row": fields.String,
    "to_row": fields.String,
})
RANGE_MODEL = API.model('Range', {
    'min': fields.Integer,
    'max': fields.Integer
})
EXTENDED_FIELD_MODEL = API.inherit('Extended_field', FIELD_MODEL, {
    "range": fields.Nested(RANGE_MODEL),
    "choice_options": fields.List(fields.String),
    "setting_autocomplete": fields.Nested(AUTOCOMPLETE_MODEL)
})

FIELD_PUT_MODEL = API.model('FieldPut', {
    "name": fields.String,
    "range": fields.Nested(RANGE_MODEL),
    "added_choice_options": fields.List(fields.String),
    "removed_choice_options": fields.List(fields.String),
    "settings_autocomplete": fields.Nested(AUTOCOMPLETE_MODEL)
})


@FIELDS_NS.route("/")
class FieldsAPI(Resource):
    """
    Field API

    url: '/fields'
    methods: GET, POST
    """

    @API.doc(
        responses={
            201: 'Created',
            401: 'Unauthorized'
        }
    )
    @API.expect(EXTENDED_FIELD_MODEL)  # pylint: disable=too-many-branches
    @login_required
    # pylint: disable=no-self-use
    def post(self):
        """
        Create new field

        :return: json
        """
        data = request.json
        is_correct, errors = FieldService.validate(data)
        if not is_correct:
            raise BadRequest(errors)

        if current_user.id != int(data["owner_id"]):
            raise Forbidden("Unexpected User")

        field_type = data['field_type']

        if field_type in (FieldType.Text.value, FieldType.Number.value):
            is_correct, errors = FieldService.validate_text_or_number(data)
            if not is_correct:
                raise BadRequest(errors)

            range_min, range_max = FieldService.check_for_range(data)

            response = FieldService.create_text_or_number_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                range_min=range_min,
                range_max=range_max)

        elif field_type == FieldType.TextArea.value:
            is_correct, errors = FieldService.validate_textarea(data)
            if not is_correct:
                raise BadRequest(errors)

            response = FieldService.create_text_area(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
            )

        elif field_type == FieldType.Radio.value:
            is_correct, errors = FieldService.validate_radio(data)
            if not is_correct:
                raise BadRequest(errors)

            response = FieldService.create_radio_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                choice_options=data['choice_options']
            )

        elif field_type == FieldType.Checkbox.value:
            is_correct, errors = FieldService.validate_checkbox(data)
            if not is_correct:
                raise BadRequest(errors)
            range_min, range_max = FieldService.check_for_range(data)

            response = FieldService.create_checkbox_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                choice_options=data['choice_options'],
                range_min=range_min,
                range_max=range_max
            )

        elif field_type == FieldType.Autocomplete.value:
            is_correct, errors = FieldService.validate_setting_autocomplete(data)
            if not is_correct:
                raise BadRequest(errors)

            response = FieldService.create_autocomplete_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                data_url=data['setting_autocomplete']['data_url'],
                sheet=data['setting_autocomplete']['sheet'],
                from_row=data['setting_autocomplete']['from_row'],
                to_row=data['setting_autocomplete']['to_row']
            )

        if response is None:
            raise BadRequest("Could not create")

        return Response(status=201)

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
        Get all user fields

        :return: json
        """
        field_list = FieldService.filter(owner_id=current_user.id)

        response = []

        # add options to field json
        for field in field_list:
            extra_options = FieldService.get_additional_options(
                field.id,
                field.field_type
            )

            field = FieldService.field_to_json(field)
            if extra_options:
                for key, value in extra_options.items():
                    field[key] = value
            response.append(field)

        return jsonify(response)


@FIELDS_NS.route("/<int:field_id>/")
class FieldAPI(Resource):
    """
    Fields API

    url: '/fields/{id}'
    methods: get, put, delete
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Bad Request',
            403: 'User is not the field owner'
        }, params={
            'field_id': 'Field id'
        }
    )
    # pylint: disable=no-self-use
    def get(self, field_id):
        """
        Get field by id

        :param field_id: field id
        :return: json
        """
        field = FieldService.get_by_id(field_id)

        if field is None:
            raise BadRequest("Field does not exist")

        if current_user.id != field.owner_id:
            raise Forbidden("Forbidden. User is not the field owner")

        field_json = FieldService.field_to_json(field)
        extra_options = FieldService.get_additional_options(field.id, field.field_type)
        if extra_options:
            for key, value in extra_options.items():
                field_json[key] = value

        return jsonify(field_json)

    @API.doc(
        responses={
            200: "OK",
            400: "Invalid syntax",
            401: "Unauthorized",
            403: "Forbidden update"
        },
        params={
            "field_id": "Specify ID of the field you want to update"
        }
    )
    @API.expect(FIELD_PUT_MODEL, validate=False)
    @login_required
    #pylint: disable = no-self-use
    def put(self, field_id):
        """
        Field PUT method

        :param field_id: ID of the field
        """
        field = FieldService.get_by_id(field_id)

        if field.owner_id != current_user.id:
            raise Forbidden("Can't update field you don't own")

        data = request.get_json()

        is_correct, errors = FieldService.validate_update_field(data)
        if not is_correct:
            raise BadRequest(errors)

        field_type = field.field_type

        if field_type in (FieldType.Number.value, FieldType.Text.value):
            range_min, range_max = FieldService.check_for_range(data)
            response = FieldService.update_text_or_number_field(
                field_id=field_id,
                name=data.get('name'),
                owner_id=field.owner_id,
                field_type=field_type,
                range_min=range_min,
                range_max=range_max
            )
            return response

        elif field_type == FieldType.TextArea.value:
            response = FieldService.update(
                field_id=field_id,
                name=data.get("name"),
                owner_id=field.owner_id,
                field_type=field_type,
                is_strict=False
            )
            response = FieldPutSchema().dump(response)

        elif field_type == FieldType.Radio.value:
            added_choice_options = data.get("added_choice_options")
            removed_choice_options = data.get("removed_choice_options")
            response = FieldService.update_radio_field(
                field_id=field_id,
                name=data.get("name"),
                owner_id=field.owner_id,
                field_type=field_type,
                added_choice_options=added_choice_options,
                removed_choice_options=removed_choice_options
            )
            return response
