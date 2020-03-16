"""
Form schemas
"""

from marshmallow import fields, validates_schema, ValidationError

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
        fields = ("id", "owner_id", "name", "title", "result_url", "is_published")

    owner_id = fields.Int(dump_only=True, data_key='ownerId')
    name = fields.Str(required=True)
    title = fields.Str(required=True)
    result_url = fields.Url(required=True, data_key='resultUrl')
    is_published = fields.Bool(required=True, data_key='isPublished')

    @validates_schema
    # pylint:disable=no-self-use
    def validate_data_url(self, data, **kwargs):
        """
        Validates url, which must be docs.google.com
        :param data:
        :param kwargs:
        :return:
        """
        result_url = data.get('result_url')
        if not validate_url(url=result_url):
            raise ValidationError('Wrong URL entered')
