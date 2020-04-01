"""
Share form celery task
"""
from app import CELERY, MAIL
from app.helper.email_generator import (
    generate_share_form_to_group_user_message,
    generate_share_form_to_user_message
)
from app.helper.socket import send_notification


def call_share_form_to_group_task(recipients, group_name, form_title, token):
    """
    Call task to share form to group users

    :param recipients: group users emails
    :param group_name: name of group to which form will be shared
    :param form_title: title of form that will be shared
    :param token: form token
    :return:
    """
    task = share_form_to_group.apply_async(
        args=[recipients, group_name, form_title, token],
        queue="share_form_to_group_queue"
    )
    message = task.get()
    send_notification(message)
    return 0


@CELERY.task(bind=True, name='ngfg.app.celery_tasks.share_form.share_form_to_group')
# pylint: disable=unused-argument
def share_form_to_group(self, recipients, group_name, form_title, token):
    """
    Send emails to group users

    """
    with MAIL.connect() as conn:
        for recipient in recipients:
            msg = generate_share_form_to_group_user_message(
                recipient,
                group_name,
                form_title,
                token
            )
            conn.send(msg)

    return f"Form '{form_title}' has been sent to '{group_name}' group!"


def call_share_form_to_users_task(recipients, form_title, token):
    """
    Call task to share form to users

    :param recipients: users emails
    :param form_title: title of form that will be shared
    :param token: form token
    """
    task = share_form_to_users.apply_async(
        args=[recipients, form_title, token],
        queue="share_form_to_users_queue"
    )
    message = task.get()
    send_notification(message)
    return 0


@CELERY.task(bind=True, name='ngfg.app.celery_tasks.share_field.share_form_to_users')
# pylint: disable=unused-argument
def share_form_to_users(self, recipients, form_title, token):
    """
    Send emails to recipients

    :param recipients: users emails
    :param form_title: title of form that will be shared
    :param token: form token
    """

    with MAIL.connect() as conn:
        for recipient in recipients:
            msg = generate_share_form_to_user_message(recipient, form_title, token)
            conn.send(msg)

    return f'Form {form_title} has been shared with users!'
