"""
Base router view.
"""
from app import APP, SERIALIZER
from app.helper.email_sender import EmailSender


@APP.route('/')
def hello_world():
    """
    example

    :return: str
    """
    EmailSender.share_field(1, ['dz000iga2000@gmail.com'])
    return 'Hello, World!'


@APP.route('/receive_field/<token>')
def receive_field(token):
    """
    example

    :return: str
    """
    field = SERIALIZER.loads(token, salt='share_field')
    return f'Field id that you\'ve ({field["recipient"]}) received: {field["field_id"]}'
