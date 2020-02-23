from flask_restx import fields, Resource
from flask import request

from app import API
from app.models import Field
from app.services.field_post import FieldPost

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
autocomplete_model = API.model('setting_autocomplete',{
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
        try:
            data = request.json
            print(data)
            FieldPost.create(**data)
            return {'success': '200'}
        except KeyError as e:
            name_space.abort(500, e.__doc__,
                             status="Could not save information",
                             statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__,
                             status="Could not save information",
                             statusCode="400")
