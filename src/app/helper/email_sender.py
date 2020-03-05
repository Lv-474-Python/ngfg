from flask_mail import Message

from app import MAIL


class EmailSender:
    """
    Sender
    """

    @staticmethod
    def send_email(recipients):
        msg = Message('subject', recipients=recipients)
        msg.body = 'text_body'
#        msg.html = '<b>html</b>_body'
        MAIL.send(msg)
