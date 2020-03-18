"""
ShareField resource API
"""
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from flask import request, jsonify, Response
from flask_restx import Resource, fields

from app import API
from app.services import SharedFieldService
from app.services import UserService, FieldService
from app.celery_tasks.share_field import call_share_field_task
from app.helper.errors import SharedFieldNotCreated

SHARED_FIELD_NS = API.namespace('shared_fields')
SHARE_FIELD_MODEL = API.model('ShareField', {
    'recipients': fields.List(fields.String),
    'fieldId': fields.Integer})


@SHARED_FIELD_NS.route("/")
class ShareFieldsAPI(Resource):
    """
    SharedFields API

    url: '/shared_fields/'
    methods: get, post
    """

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
        }
    )
    @API.expect(SHARE_FIELD_MODEL)
    @login_required
    #pylint: disable=no-self-use
    def post(self):
        """
        Share field to a list of users
        """
        data = request.json
        is_correct, errors = SharedFieldService.validate_post_data(data=data)
        if not is_correct:
            raise BadRequest(errors)
        emails = data['recipients']
        users = []

        for email in emails:
            user = UserService.get_by_email(email=email)
            if user is None or not user.is_active:
                raise BadRequest("Can't share field to nonexistent or inactive users")
            if user.id == current_user.id:
                raise BadRequest("Can't share field with yourself")
            users.append(user)

        field = FieldService.get_by_id(
            field_id=data['fieldId']
        )
        if field is None:
            raise BadRequest("Field doesn't exist")
        if field.owner_id != current_user.id:
            raise BadRequest("Can't share field that doesn't belong to you")

        shared_fields = []

        for user in users:
            shared_field_instance = SharedFieldService.get_by_user_and_field(
                user_id=user.id,
                field_id=field.id
            )
            if shared_field_instance is not None:
                raise BadRequest("Can't share field twice")
            shared_field = SharedFieldService.create(
                user_id=user.id,
                field_id=field.id,
                owner_id=current_user.id
            )
            if shared_field is None:
                raise SharedFieldNotCreated()
            shared_fields.append(shared_field)

        field_json = FieldService.field_to_json(
            data=field,
            many=False
        )
        shared_fields_json = SharedFieldService.response_to_json(
            data=shared_fields,
            many=True
        )

        call_share_field_task(
            recipients=emails,
            field=field_json
        )

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
    #pylint: disable=no-self-use
    def get(self):
        """
        Get all fields that were shared by given user
        """
        shared_fields = SharedFieldService.filter(
            owner_id=current_user.id
        )
        shared_fields_json = SharedFieldService.response_to_json(
            data=shared_fields,
            many=True
        )
        response = jsonify({'sharedFields': shared_fields_json})
        response.status_code = 200
        return response


@SHARED_FIELD_NS.route("/<int:field_id>/user/<int:user_id>")
class SharedFieldAPI(Resource):
    """
    SharedField API

    url: '/shared_fields/{field_id}/user/{user_id}'
    methods: get, delete
    """

    @API.doc(
        responses={
            200: 'OK',
            400: 'Invalid data'
        }, params={
            'field_id': 'Specify the id of the field you shared',
            'user_id': 'Specify the id of the user to whom you shared the field to'
        }
    )
    @login_required
    #pylint: disable=no-self-use
    def get(self, field_id, user_id):
        """
        Get shared field by field id
        """
        field = FieldService.get_by_id(field_id)
        if field is None:
            raise BadRequest("No such field")
        user = UserService.get_by_id(user_id)
        if user is None:
            raise BadRequest("No such user")
        shared_field = SharedFieldService.get_by_user_and_field(
            user_id=user_id,
            field_id=field_id
        )
        if shared_field is None:
            raise BadRequest("It seems like you haven't shared this field with that user yet")
        shared_field_json = SharedFieldService.response_to_json(
            data=shared_field,
            many=False
        )
        response = jsonify(shared_field_json)
        response.status_code = 200
        return response

    @API.doc(
        responses={
            204: 'No content',
            400: 'Invalid syntax',
            401: 'Unauthorized',
            403: 'Forbidden deletion',
        },
        params={
            'field_id': 'ID of the shared field',
            'user_id': 'ID of the user the field was shared to'
        }
    )
    #pylint: disable=no-self-use
    def delete(self, field_id, user_id):
        """
        Unshare certain field from a certain user

        :param field_id: ID of the shared field
        :param user_id: ID of the user the field was shared to
        """
        field = FieldService.get_by_id(field_id)
        if field is None:
            raise BadRequest("Can't unshare field that doesn't exist")
        if field.owner_id != current_user.id:
            raise BadRequest("Can't unshare field that doesn't belong to you")
        shared_field = SharedFieldService.get_by_user_and_field(
            user_id=user_id,
            field_id=field_id
        )
        if shared_field is None:
            raise BadRequest("Can't unshare, instance doesn't exist")

        is_deleted = bool(SharedFieldService.delete(shared_field.id))
        if not is_deleted:
            raise BadRequest("Failed to unshare")
        return Response(status=204)
