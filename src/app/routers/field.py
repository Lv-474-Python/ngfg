"""
Field router.
"""
from flask import request, jsonify, Response
from flask_restx import fields, Resource
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, Forbidden
from app.schemas import BasicField

from app import API
from app.helper.enums import FieldType
from app.services import FieldService, UserService

FIELDS_NS = API.namespace('fields', description='Field APIs')

FIELD_MODEL = API.model('Field', {
    'name': fields.String(required=True),
    'fieldType': fields.Integer(required=True),
    'isStrict': fields.Boolean(required=False)
})
AUTOCOMPLETE_MODEL = API.model('settingAutocomplete', {
    "dataUrl": fields.Url,
    "sheet": fields.String,
    "fromRow": fields.String,
    "toRow": fields.String,
})
RANGE_MODEL = API.model('Range', {
    'min': fields.Integer,
    'max': fields.Integer
})
EXTENDED_FIELD_MODEL = API.inherit('Extended_field', FIELD_MODEL, {
    "range": fields.Nested(RANGE_MODEL),
    "choiceOptions": fields.List(fields.String),
    "settingAutocomplete": fields.Nested(AUTOCOMPLETE_MODEL)
})

FIELD_PUT_MODEL = API.model('FieldPut', {
    "updatedName": fields.String,
    "range": fields.Nested(RANGE_MODEL),
    "addedChoiceOptions": fields.List(fields.String),
    "removedChoiceOptions": fields.List(fields.String),
    "updatedAutocomplete": fields.Nested(AUTOCOMPLETE_MODEL),
    "deleteRange": fields.Boolean(default=False),
    "isStrict": fields.Boolean
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
        is_correct, errors = FieldService.validate_post_field(data=data, user=current_user.id)
        if not is_correct:
            raise BadRequest(errors)
        field_type = data.get('fieldType')

        if field_type in (FieldType.Text.value, FieldType.Number.value):
            is_correct, errors = FieldService.validate_text_or_number(data)
            if not is_correct:
                raise BadRequest(errors)

            range_min, range_max = FieldService.check_for_range(data)

            field = FieldService.create_text_or_number_field(
                name=data.get('name'),
                owner_id=current_user.id,
                field_type=field_type,
                is_strict=data.get('isStrict', False),
                range_min=range_min,
                range_max=range_max)

        elif field_type == FieldType.TextArea.value:
            is_correct, errors = FieldService.validate_textarea(data)
            if not is_correct:
                raise BadRequest(errors)

            field = FieldService.create_text_area(
                name=data.get('name'),
                owner_id=current_user.id,
                field_type=field_type,
            )

        elif field_type == FieldType.Radio.value:
            is_correct, errors = FieldService.validate_radio(data)
            if not is_correct:
                raise BadRequest(errors)

            field = FieldService.create_radio_field(
                name=data.get('name'),
                owner_id=current_user.id,
                field_type=field_type,
                choice_options=data.get('choiceOptions')
            )

        elif field_type == FieldType.Checkbox.value:
            is_correct, errors = FieldService.validate_checkbox(data)
            if not is_correct:
                raise BadRequest(errors)
            range_min, range_max = FieldService.check_for_range(data)

            field = FieldService.create_checkbox_field(
                name=data.get('name'),
                owner_id=current_user.id,
                field_type=field_type,
                choice_options=data.get('choiceOptions'),
                range_min=range_min,
                range_max=range_max
            )

        elif field_type == FieldType.Autocomplete.value:
            is_correct, errors = FieldService.validate_setting_autocomplete(data)
            if not is_correct:
                raise BadRequest(errors)
            setting_autocomplete = data.get('settingAutocomplete')
            field = FieldService.create_autocomplete_field(
                name=data.get('name'),
                owner_id=current_user.id,
                field_type=field_type,
                data_url=setting_autocomplete.get('dataUrl'),
                sheet=setting_autocomplete.get('sheet'),
                from_row=setting_autocomplete.get('fromRow'),
                to_row=setting_autocomplete.get('toRow')
            )

        if field is None:
            raise BadRequest("Could not create")

        response = jsonify(field)
        response.status_code = 201
        return response

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

        # append shared fields for this user
        shared_fields = FieldService.get_shared_fields(user_id=current_user.id)
        field_list.extend(shared_fields)

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

            owner = UserService.get_by_id(field['ownerId'])
            field['owner'] = UserService.to_json(owner)
            if field['ownerId'] == current_user.id:
                field['owner']['current'] = True

            response.append(field)

        return jsonify({"fields": response})


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
    @login_required
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
    # pylint: disable = no-self-use
    # pylint: disable=too-many-branches
    def put(self, field_id):
        """
        Field PUT method

        :param field_id: ID of the field
        """
        field = FieldService.get_by_id(field_id)

        if field is None:
            raise BadRequest()

        if field.owner_id != current_user.id:
            raise Forbidden("Can't update field you don't own")

        form_membership = FieldService.check_form_membership(field_id)
        if form_membership:
            raise Forbidden("Can't update field that's already in use")

        data = request.get_json()

        is_correct, errors = FieldService.validate_update_field(
            data=data,
            user=current_user.id,
            field_id=field_id
        )
        if not is_correct:
            raise BadRequest(errors)
        field_type = field.field_type

        if field_type in (FieldType.Number.value, FieldType.Text.value):
            is_correct, errors = FieldService.validate_text_or_number_update(
                data=data,
                field_type=field_type)
            if not is_correct:
                raise BadRequest(errors)

            range_min, range_max = FieldService.check_for_range(data)

            updated_field = FieldService.update_text_or_number_field(
                field_id=field_id,
                name=data.get('updatedName'),
                range_min=range_min,
                range_max=range_max,
                is_strict=data.get('isStrict'),
                delete_range=data.get('deleteRange')
            )

        elif field_type == FieldType.TextArea.value:
            is_correct, errors = FieldService.validate_textarea_update(data)
            if not is_correct:
                raise BadRequest(errors)

            data = FieldService.update(
                field_id=field_id,
                name=data.get("updatedName"),
                is_strict=False
            )
            updated_field = BasicField().dump(data)

        elif field_type == FieldType.Radio.value:
            is_correct, errors = FieldService.validate_radio_update(data, field_id)
            if not is_correct:
                raise BadRequest(errors)

            updated_field = FieldService.update_radio_field(
                field_id=field_id,
                name=data.get("updatedName"),
                added_choice_options=data.get("addedChoiceOptions"),
                removed_choice_options=data.get("removedChoiceOptions")
            )

        elif field_type == FieldType.Autocomplete.value:
            is_correct, errors = FieldService.validate_autocomplete_update(data)
            if not is_correct:
                raise BadRequest(errors)

            settings_autocomplete = data.get('updatedAutocomplete')
            updated_field = FieldService.update_autocomplete_field(
                field_id=field_id,
                name=data.get('updatedName'),
                data_url=settings_autocomplete.get('dataUrl'),
                sheet=settings_autocomplete.get('sheet'),
                from_row=settings_autocomplete.get('fromRow'),
                to_row=settings_autocomplete.get('toRow')
            )

        elif field_type == FieldType.Checkbox.value:
            is_correct, errors = FieldService.validate_checkbox_update(data, field_id)
            if not is_correct:
                raise BadRequest(errors)

            range_min, range_max = FieldService.check_for_range(data)
            added_choice_options = data.get("addedChoiceOptions")
            removed_choice_options = data.get("removedChoiceOptions")
            updated_field = FieldService.update_checkbox_field(
                field_id=field_id,
                name=data.get("updatedName"),
                range_max=range_max,
                range_min=range_min,
                added_choice_options=added_choice_options,
                removed_choice_options=removed_choice_options,
                delete_range=data.get("deleteRange"),
            )

        if updated_field is None:
            raise BadRequest("Couldn't update")

        response = jsonify(updated_field)
        response.status_code = 200
        return response

    @API.doc(
        responses={
            200: 'OK',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'User is not the field owner'
        }, params={
            'field_id': 'Field id'
        }
    )
    @login_required
    # pylint: disable=no-self-use
    def delete(self, field_id):
        """
        Delete field

        :param field_id:
        :return:
        """
        field = FieldService.get_by_id(field_id=field_id)
        if field is None:
            raise BadRequest('Field does not exist')
        if current_user.id != field.owner_id:
            raise Forbidden('Forbidden. User is not the field owner')
        form_membership = FieldService.check_form_membership(field_id)
        if form_membership:
            raise Forbidden("Can't updated field that's already in use")
        delete = FieldService.delete(field_id=field_id)
        is_deleted = bool(delete)
        if not is_deleted:
            raise BadRequest("Could not delete field")

        return Response(status=200)
