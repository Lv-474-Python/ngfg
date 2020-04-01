"""
Share form resource API
"""

from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from flask import request, jsonify
from flask_restx import Resource, fields

from app import API
from app.services import SharedFormService, GroupService, FormService, TokenService
from app.helper.jwt_helper import generate_token
from app.schemas import SharedFormFlagsSchema, SharedFormPostSchema
from app.celery_tasks.share_form import (
    call_share_form_to_group_task,
    call_share_form_to_users_task
)

SHARED_FORM_NS = API.namespace('shared_forms')
SHARE_FIELD_POST_MODEL = API.model('ShareForm', {
    'groups_ids': fields.List(fields.Integer),
    'users_emails': fields.List(fields.String),
    'nbf': fields.DateTime(dt_format='iso8601'),
    'exp': fields.DateTime(dt_format='iso8601')
})


@SHARED_FORM_NS.route("/<int:form_id>/")
class SharedFormAPI(Resource):
    """
    SharedForms API

    url: '/shared_forms/{form_id}'
    methods: get, post
    """

    @API.doc(
        responses={
            201: 'Created',
            400: 'Invalid data',
            401: 'Unauthorized',
        },
        params={
            'form_id': 'Specify the id of the form you want to share',
        }
    )
    @API.expect(SHARE_FIELD_POST_MODEL)
    @login_required
    #pylint: disable=no-self-use
    def post(self, form_id):
        """
        Share form to group or list of emails

        :param form_id: id of form that will be shared
        """
        data = request.json
        is_correct, errors = SharedFormService.validate_data(SharedFormPostSchema, data)
        if not is_correct:
            raise BadRequest(errors)

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form doesn't exist")
        if form.owner_id != current_user.id:
            raise BadRequest("You can't share form that doesn't belong to you")

        groups_ids = data.get('groups_ids')
        errors = GroupService.check_whether_groups_exist(groups_ids)
        if errors:
            raise BadRequest(errors)

        # handling users_emails
        payload = SharedFormService.get_token_initial_payload(
            form_id=form_id,
            exp=data.get('exp'),
            nbf=data.get('nbf')
        )

        response = {
            'groupsTokens': {},
            'usersToken': None
        }

        users_emails = data.get('users_emails')
        if users_emails:
            token = generate_token(payload)
            token_instance = TokenService.create(
                token=token,
                form_id=form_id
            )

            if token_instance is None:
                response['usersToken'] = None
            else:
                response['usersToken'] = token_instance.token

                # send emails with token to users_emails
                call_share_form_to_users_task(
                    users_emails,
                    form.title,
                    token
                )

        # handling groups_ids
        for group_id in groups_ids:
            group = GroupService.get_by_id(group_id)
            if group is None:
                response['groupsTokens'][str(group_id)] = None
                continue

            users = GroupService.get_users_by_group(group_id)
            if users is None:
                response['groupsTokens'][str(group_id)] = None
                continue
            users_emails = list(map(lambda user: user['email'], users))

            group_payload = dict(payload)
            group_payload['group_id'] = group_id
            token = generate_token(group_payload)

            token_instance = TokenService.create(
                token=token,
                form_id=form_id
            )
            if token_instance is None:
                response['groupsTokens'][str(group_id)] = None
                continue

            response['groupsTokens'][str(group_id)] = token_instance.token

            # send emails with token to group_users_emails
            call_share_form_to_group_task(
                users_emails,
                group.name,
                form.title,
                token
            )

        # Чи в нас буде різні таски на відправки групам і відправку
        # Чи в нас буде типу що дістаєш всіх всіх юзерів і відправляєш
        # Поки різні бо хз що там з тим перехваткою тасок і типу моніторингу

        response = jsonify(response)
        response.status_code = 201
        return response


    @API.doc(
        responses={
            201: 'Created',
            401: 'Unauthorized',
        },
        params={
            'nbf': 'Set token nbf (Not Before Time)',
            'exp': 'Set token exp (Expiration Time)'
        }
    )
    @login_required
    #pylint: disable=no-self-use
    def get(self, form_id):
        """
        Get token to pass form

        :param form_id: id of form that will be shared
        """
        args = request.args
        is_correct, errors = SharedFormService.validate_data(SharedFormFlagsSchema, args)
        if not is_correct:
            raise BadRequest(errors)

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form doesn't exist")
        if form.owner_id != current_user.id:
            raise BadRequest("Can't share form that doesn't belong to you")

        payload = SharedFormService.get_token_initial_payload(
            form_id=form_id,
            exp=args.get('exp'),
            nbf=args.get('nbf')
        )
        token = generate_token(payload)
        token_instance = TokenService.create(
            token=token,
            form_id=form_id
        )

        if token_instance is None:
            raise BadRequest("Cannot create token instance")

        response = jsonify({'token': token_instance.token})
        response.status_code = 201
        return response

# celery -A app worker --loglevel=info -Q share_form_to_group_queue,share_form_to_users_queue
