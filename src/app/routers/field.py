"""
Field router.
"""
from flask import request, jsonify
from flask_restx import fields, Resource
from flask_login import current_user
from app import API
from app.services.field_crud import FieldOperation, FieldService

NS_FIELDS = API.namespace('fields', description='NgFg APIs')

MAIN_MODEL = API.model('fields', {
    'name': fields.String(required=True),
    'owner_id': fields.Integer(required=True),
    'field_type': fields.Integer(required=True)
})
AUTOCOMPLETE_MODEL = API.model('setting_autocomplete', {
    "data_url": fields.String,
    "sheet": fields.String,
    "from_row": fields.String,
    "to_row": fields.String,
})
RANGE_MODEL = API.model('range', {
    'min': fields.Integer,
    'max': fields.Integer
})

EXTENDED_MODEL = API.inherit('extended_field', MAIN_MODEL, {
    "range": fields.Nested(RANGE_MODEL),
    "choice_options": fields.List(fields.String),
    "setting_autocomplete": fields.Nested(AUTOCOMPLETE_MODEL)
})


@NS_FIELDS.route("/")
class FieldAPI(Resource):
    """
    Field API
    """

    @API.expect(EXTENDED_MODEL)
    # pylint: disable=no-self-use
    def post(self):
        """
        Field POST method

        :return: json
        """
        req = request.json
        data = FieldOperation.create(**req)

        return {'data': data, 'SUCCESS': 'OK'}

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
                                                               field['field_type'])
            if extra_options:
                for key, value in extra_options.items():
                    field[key] = value

        return jsonify(fields_json)
