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
from app.helper.errors import SettingAutocompleteNotSend
from app.services.field_crud import FieldOperation, FieldService

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


@FIELDS_NS.route("")
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
        errors = FieldService.validate(request.json)
        if errors:
            raise BadRequest('Invalid parameters')

        data = request.json

        field_type = data['field_type']

        if field_type in (FieldType.Text.value, FieldType.Number.value):
            range_min, range_max = None, None
            if range_instance := data.get('range'):
                range_min = range_instance.get('min')
                range_max = range_instance.get('max')

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

        elif field_type in (FieldType.Radio.value, FieldType.Checkbox.value):

            response = FieldService.create_choice_option_field(
                name=data['name'],
                owner_id=data['owner_id'],
                field_type=data['field_type'],
                choice_options=data['choice_options']
            )

        elif field_type == FieldType.Autocomplete.value:
            if errors := FieldService.validate_setting_autocomplete(data):
                print(errors)
                raise SettingAutocompleteNotSend('SettingAutocompleteNotSend')
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
        field_list = FieldOperation.get_user_fields(current_user.id)
        fields_json = FieldService.to_json(field_list, many=True)

        # add options to field json
        for field in fields_json:
            extra_options = FieldOperation.check_other_options(field['id'],
                                                               field[
                                                                   'field_type'])
            if extra_options:
                for key, value in extra_options.items():
                    field[key] = value

        return jsonify(fields_json)
