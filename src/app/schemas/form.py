"""
Form schemas
"""

from marshmallow import fields, validates, ValidationError

from app import MA
from app.helper.google_docs_url_validator import validate_url


class FormSchema(MA.Schema):
    """
    Form schema

    :param name - str
    :param title - str
    :param result_url - url
    :param is_published - bool
    """

    class Meta:
        """
        Form schema meta
        """
        fields = ("id", "owner_id", "name", "title", "result_url", "is_published", "created")

    owner_id = fields.Int(dump_only=True, data_key='ownerId')
    name = fields.Str(required=True)
    title = fields.Str(required=True)
    result_url = fields.Url(required=True, data_key='resultUrl')
    is_published = fields.Bool(required=True, data_key='isPublished')

    @validates("result_url")
    # pylint:disable=no-self-use
    def validate_url_data(self, value):
        """
        Validates url, which must be docs.google.com
        :param value:
        :return:
        """
        if value == "":
            raise ValidationError("Missing data for required field.")
        elif not validate_url(url=value):
            raise ValidationError('Wrong URL entered.')

    @validates("name")
    def validate_name_data(self, value):
        """
        Validates name, which can't be an empty string
        :param value: entered name
        :return: raise error if value is not valid
        """
        if value == "":
            raise ValidationError("Missing data for required field.")

    @validates("title")
    def validate_title_data(self, value):
        """
        Validates title, which can't be an empty string
        :param value: entered title
        :return: raise error if value is not valid
        """
        if value == "":
            raise ValidationError("Missing data for required field.")
