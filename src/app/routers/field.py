"""
Field router.
"""
from flask import request, jsonify
from flask_restx import fields, Resource
from flask_login import current_user
from werkzeug.exceptions import BadRequest
from app.models.field import FieldSchema
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
    "data_url": fields.String,
    "sheet": fields.String,
    "from_row": fields.String,
    "to_row": fields.String,
})
RANGE_MODEL = API.model('Range', {
    'min': fields.Integer,
    'max': fields.Integer
})

EXTENDED_MODEL = API.inherit('Extended_field', FIELD_MODEL, {
    "range": fields.Nested(RANGE_MODEL),
    "choice_options": fields.List(fields.String),
    "setting_autocomplete": fields.Nested(AUTOCOMPLETE_MODEL)
})


@FIELDS_NS.route("/")
class FieldAPI(Resource):
    """
    Field API
    """

    @API.expect(FIELD_MODEL)
    # pylint: disable=no-self-use
    def post(self):
        """
        Field POST method

        :return: json
        """
        is_correct, errors = FieldService.validate(request.json)
        if not is_correct:
            raise BadRequest(errors)

        data = request.json

        field_type = data['field_type']

        if field_type in (FieldType.Text.value, FieldType.Number.value):
            is_correct, errors = FieldService.validate_text_or_number(request.json)
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
            response = FieldService.create(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
            )
            response = FieldSchema().dump(response)

        elif field_type == FieldType.Radio.value:
            is_correct, errors = FieldService.validate_radio(request.json)
            if not is_correct:
                raise BadRequest(errors)

            response = FieldService.create_radio_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                choice_options=data['choice_options']
            )

        elif field_type == FieldType.Checkbox.value:
            is_correct, errors = FieldService.validate_checkbox(request.json)
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
            is_correct, errors = FieldService.validate_setting_autocomplete(request.json)
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

        return jsonify(response)

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
            404: 'Field not found'
        }
    )
    # pylint: disable=no-self-use
    def get(self):
        """
        Field GET method

        :return: json
        """
        field_list = FieldService.filter(owner_id=current_user.id)

        response = []

        # add options to field json
        for field in field_list:
            # Text area does not have additional options
            if field.field_type == FieldType.TextArea.value:
                continue

            extra_options = FieldService.check_other_options(
                field.id,
                field.field_type
            )

            field = FieldService.field_to_json(field)
            if extra_options:
                for key, value in extra_options.items():
                    field[key] = value
            response.append(field)

        return jsonify(response)
