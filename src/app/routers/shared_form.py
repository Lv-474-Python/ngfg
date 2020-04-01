"""
Share form resource API
"""

from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from flask import request, jsonify, Response
from flask_restx import Resource, fields

from app import API
from app.services import SharedFormService, GroupService, FormService
from app.helper.jwt_helper import generate_token, decode_token
from app.schemas import SharedFormPostSchema, SharedFormGetSchema
from app.celery_tasks.share_form import (
    call_share_form_to_group_task,
    call_share_form_to_users_task
)

# from app.helper.errors import SharedFieldNotCreated

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
        """
        data = request.json
        is_correct, errors = SharedFormService.validate_data(SharedFormPostSchema, data)
        if not is_correct:
            raise BadRequest(errors)

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form doesn't exist")
        if form.owner_id != current_user.id:
            raise BadRequest("Can't share form that doesn't belong to you")

        # import pdb; pdb.set_trace()

        #TODO - валідація що exp не може бути меншою за nbf

        groups_ids = data.get('groups_ids')
        users_emails = data.get('users_emails')

        # check whether groups exist
        groups = []
        groups_errors = []
        for group_id in groups_ids:
            group = GroupService.get_by_id(group_id)
            if group is None:
                groups_errors.append(f"Group {group_id} doesn't exist")
            groups.append(group)
            # groups.append({'group_id': group_id, 'users': users})

        if groups_errors:
            raise BadRequest(groups_errors)

        # set token payload
        payload = {
            'form_id': form_id,
            'group_id': None,
        }

        exp = data.get('exp')
        if exp is not None:
            exp = SharedFormService.convertStringToDateTime(exp)
            payload['exp'] = exp

        nbf = data.get('nbf')
        if nbf is not None:
            nbf = SharedFormService.convertStringToDateTime(nbf)
            payload['nbf'] = nbf

        #TODO - якщо не створиться то скіпати

        # send emails and set response json
        response_json = {
            'groupsTokens': {},
            'usersToken': None
        }

        for group in groups:
            group_users = GroupService.get_users_by_group(group.id)
            #TODO - подумай тут добре
            if not group_users:
                continue

            group_users_emails = list(map(lambda user: user['email'], group_users))

            group_payload = dict(payload)
            group_payload['group_id'] = group.id
            group_token = generate_token(group_payload)

            # if token is not None: response['groups_tokens'][str(group['group_id'])] = group_token.value
            # group_token = token.value if token is not None else None
            response_json['groupsTokens'][str(group.id)] = group_token # group_token.value

            # send emails by group_token to group_users_emails
            # якщо є токен то шар
            call_share_form_to_group_task(
                group_users_emails,
                group.name,
                form.title,
                group_token
            )

        if users_emails:
            token = generate_token(payload)
            # create token instance

            response_json['usersToken'] = token # token.value

            # send emails by token to users_emails 
            call_share_form_to_users_task(
                users_emails,
                form.title,
                token
            )


        #TODO - чи в нас буде різні таски на відправки групам і відправку. Чи в нас буде типу що дістаєш всіх всіх юзерів і відправляєш











        # for email in emails:
        #     user = UserService.get_by_email(email=email)
        #     if user is None or not user.is_active:
        #         raise BadRequest("Can't share field to nonexistent or inactive users")
        #     if user.id == current_user.id:
        #         raise BadRequest("Can't share field with yourself")
        #     users.append(user)


        # shared_fields = []

        # for user in users:
        #     shared_field_instance = SharedFieldService.get_by_user_and_field(
        #         user_id=user.id,
        #         field_id=field.id
        #     )
        #     if shared_field_instance is not None:
        #         raise BadRequest("Can't share field twice")
        #     shared_field = SharedFieldService.create(
        #         user_id=user.id,
        #         field_id=field.id,
        #         owner_id=current_user.id
        #     )
        #     if shared_field is None:
        #         raise SharedFieldNotCreated()
        #     shared_fields.append(shared_field)

        # field_json = FieldService.field_to_json(
        #     data=field,
        #     many=False
        # )
        # shared_fields_json = SharedFieldService.response_to_json(
        #     data=shared_fields,
        #     many=True
        # )

        # call_share_field_task(
        #     recipients=emails,
        #     field=field_json
        # )

        response = jsonify(response_json)
        response.status_code = 201
        return response


    @API.doc(
        responses={
            201: 'OK',
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
        """
        # validate data
        args = request.args
        is_correct, errors = SharedFormService.validate_data(SharedFormGetSchema, args)
        if not is_correct:
            raise BadRequest(errors)

        form = FormService.get_by_id(form_id)
        if form is None:
            raise BadRequest("Form doesn't exist")
        if form.owner_id != current_user.id:
            raise BadRequest("Can't share form that doesn't belong to you")

        # generate token
        payload = {
            'form_id': form_id,
            'group_id': None,
        }

        exp = args.get('exp')
        if exp is not None:
            exp = SharedFormService.convertStringToDateTime(exp)
            payload['exp'] = exp

        nbf = args.get('nbf')
        if nbf is not None:
            nbf = SharedFormService.convertStringToDateTime(nbf)
            payload['nbf'] = nbf

        token = generate_token(payload)

        import pdb; pdb.set_trace()

        # створи токен 

        response = jsonify({'token': token})
        response.status_code = 201
        return response


# EXP i NBF - різниця в 3 години якщо що (-3 години)
# я передаю 11 годину, генерую токен, декодую, беру timestamp, переводжу, пише 14 година)

# 'nbf': datetime.utcnow() + timedelta(seconds=60), # 1min
# 'exp': datetime.utcnow() + timedelta(seconds=300) # 5min



# celery -A app worker --loglevel=info -Q share_form_to_group_queue,share_form_to_users_queue