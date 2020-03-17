"""
ShareField resource API
"""
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest

from app import API
from flask import request, jsonify
from flask_restx import Resource, fields
import jwt
from app.services import SharedFieldService
from app.services import UserService, FieldService
from app.celery_tasks.share_field import call_share_field_task
from app.config import SECRET_KEY
from app.helper.constants import JWT_ALGORITHM
from app.schemas import SharedFieldSchema
from app.helper.errors import SharedFieldNotCreated

SHARED_FIELD_NS = API.namespace('shared_fields')
SHARE_FIELD_MODEL = API.model('ShareField', {
    'recipients': fields.List(fields.String),
    'fieldId': fields.Integer
    }
)


@SHARED_FIELD_NS.route("/shared")
class ShareFieldAPI(Resource):
    @API.doc(
        responses={
            201: 'Created',
            401: 'Unauthorized'
        }
    )
    @API.expect(SHARE_FIELD_MODEL)
    @login_required
    def post(self):
        data = request.json
        emails = data['recipients']
        users = []
        for email in emails:
            user = UserService.get_by_email(email=email)
            if user is None or not user.is_active:
                raise BadRequest("Can't share field to nonexistent or inactive users")
            elif user.id == current_user.id:
                raise BadRequest("Can't share field with yourself")
            users.append(user)
        field = FieldService.get_by_id(
            field_id=data['fieldId']
        )
        if field is None:
            raise BadRequest("Field doesn't exist")
        shared_fields_json = []
        for user in users:
            shared_field_instance = SharedFieldService.create(user_id=user.id, field_id=field.id)
            if shared_field_instance is None:
                raise SharedFieldNotCreated()
            shared_fields_json.append(SharedFieldService.response_to_json(
                data=shared_field_instance,
                many=False
            ))
        call_share_field_task(recipients=emails, field=field)
        response = jsonify({"sharedFields": shared_fields_json})
        response.status_code = 201
        return response

    @API.doc(
        responses={
            200: 'OK',
            401: 'Unauthorized',
        }
    )
    @login_required
    def get(self):
        pass