"""
SettingAutocomplete schemas
"""
from marshmallow import fields, validates_schema, ValidationError

from app import MA
from urllib.parse import urlparse


class SettingAutocompleteSchema(MA.Schema):
    """
    Setting autocomplete schema
    """

    class Meta:
        """
        Setting autocomplete schema meta
        """
        fields = ("data_url", "sheet", "from_row", "to_row")

    data_url = fields.Url(required=True, data_key="dataUrl")
    sheet = fields.Str(required=True)
    from_row = fields.Str(required=True, data_key="fromRow")
    to_row = fields.Str(required=True, data_key="toRow")

    @validates_schema
    def validate_data_url(self, data, **kwargs):
        parsed_url = urlparse(data.get('data_url'))
        if parsed_url.netloc != 'docs.google.com':
            raise ValidationError('You entered wrong url')

    @validates_schema
    def validate_rows(self, data, **kwargs):
        from_row = data.get('from_row')
        to_row = data.get('to_row')
        if not from_row.isalnum() or not to_row.isalnum():
            raise ValidationError('Wrong entered row limits')
        if from_row.isnumeric() or to_row.isnumeric():
            raise ValidationError('Entered only row/rows without column')
