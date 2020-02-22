from flask_restx import fields, Resource
from flask import request

from app import API
from app.models import Field

name_space = API.namespace('FIELD_API', description='NgFg APIs')
ns_forms = API.namespace('fields', description='NgFg APIs')

model = API.model('fields', {
    'name': fields.String(required=True, description="Name of the field", help="Name cannot be blank."),
    'owner_id': fields.Integer(required=False, description="ID of owner", help="Name cannot be blank."),
    'field_type': fields.Integer(required=True, description="Type of field", help="Name cannot be blank.")
})


@name_space.route("/")
class FieldCRUD(Resource):
    @API.expect(model)
    def post(self):
        try:
            name = request.json['name']
            owner_id = request.json['owner_id']
            field_type = request.json['field_type']
            print(request.json)


            return {
                "name": name,
                "owner_id": owner_id,
                "field_type": field_type
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__,
                             status="Could not save information",
                             statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__,
                             status="Could not save information",
                             statusCode="400")
