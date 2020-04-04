"""
Share field celery task
"""

from flask_login import current_user

from app import CELERY, MAIL
from app.helper.email_generator import generate_share_field_message
from .send_notification import send_notification


def call_share_field_task(recipients, field):
    """
    Send email to share field

    :param recipients:
    :param field:
    :return:
    """
    share_field.apply_async(
        args=[recipients, field],
        link=[send_notification.s(current_user.email)]
    )
    return 0


@CELERY.task(name='ngfg.app.celery_tasks.share_field.share_field')
def share_field(recipients, field):
    """
    Send emails to recipients

    :param self:
    :param recipients:
    :param field:
    :return:
    """

    with MAIL.connect() as conn:
        for recipient in recipients:
            msg = generate_share_field_message(recipient, field)
            conn.send(msg)

    return 'Field ' + field['name'] + ' have been sent!'
