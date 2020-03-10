"""
Share field celery task
"""
from app import CELERY, MAIL
from app.helper.email_generator import generate_share_field_message


def call_share_field_task(recipients, field):
    """
    Send email to share field

    :param recipients:
    :param field:
    :return:
    """
    share_field.apply_async(args=[recipients, field], queue="share_field_queue")

    return 0


@CELERY.task(bind=True, name='ngfg.app.celery_tasks.share_field.share_field')
# pylint: disable=unused-argument
def share_field(self, recipients, field):
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
    return 0
