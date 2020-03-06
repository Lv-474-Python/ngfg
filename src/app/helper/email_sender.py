from flask import render_template, url_for
from flask_mail import Message


from app import MAIL, SERIALIZER


class EmailSender:
    """
    Sender
    """

    @staticmethod
    def send_email(recipients):
        msg = Message('subject', recipients=recipients)
        msg.html = '<b>html</b>_body'
        MAIL.send(msg)

    @staticmethod
    def share_field(field_id, recipients):

        with MAIL.connect() as conn:
            for recipient in recipients:
                token = SERIALIZER.dumps({'recipient': recipient, 'field_id': field_id},
                                         salt='share_field')
                link = url_for('receive_field', token=token, _external=True)
                msg = Message('Shared Field', recipients=[recipient])
                msg.html = f'<h3> To add field to your collection, click this link: {link}</h3>'
                conn.send(msg)
