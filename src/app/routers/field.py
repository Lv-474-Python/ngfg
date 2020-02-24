from flask_restx import fields, Resource
from flask import request

from app import API
from app.services.field_crud import FieldOperation, FieldService
from flask import jsonify
from flask_login import current_user

name_space = API.namespace('FIELD_API', description='NgFg APIs')
ns_forms = API.namespace('fields', description='NgFg APIs')

# main_model = API.model('fields', {
#     'name': fields.String(required=True, description="Name of the field", help="Name cannot be blank."),
#     'owner_id': fields.Integer(required=False, description="ID of owner", help="Name cannot be blank."),
#     'field_type': fields.Integer(required=True, description="Type of field", help="Name cannot be blank.")
# })
main_model = API.model('fields', {
    'name': fields.String,
    'owner_id': fields.Integer,
    'field_type': fields.Integer
})
autocomplete_model = API.model('setting_autocomplete', {
    "data_url": fields.String,
    "sheet": fields.String,
    "from_row": fields.String,
    "to_row": fields.String,
})

extended_model = API.inherit('extended_field', main_model, {
    "range_max": fields.Integer,
    "range_min": fields.Integer,
    "choice_options": fields.List(fields.String),
    "setting_autocomplete": fields.Nested(autocomplete_model)
})


@name_space.route("/")
class FieldAPI(Resource):
    @API.expect(main_model)
    def post(self):
        req = request.get_json()
        print(req)
        FieldOperation.create(**req)
        return {'success': 'kono Dio da'}

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
            404: 'Field not found'
        }
    )
    def get(self):

        fields = FieldOperation.get_user_fields(current_user.id)

        fields_json = FieldService.to_json(fields, many=True)
        # add options to field json
        for field in fields_json:
            extra_options = FieldOperation.check_other_options(field['id'], field['field_type'])
            if extra_options:
                for key, value in extra_options.items():
                    field[key] = value
        print(fields_json)
        return jsonify(fields_json)
