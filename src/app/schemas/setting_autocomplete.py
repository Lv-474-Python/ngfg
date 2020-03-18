"""
SettingAutocomplete schemas
"""

from marshmallow import fields, validates_schema, ValidationError

from app import MA
from app.helper.google_docs_url_validator import validate_url
from app.helper.row_validation import validate_row


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
    # pylint:disable=no-self-use
    def validate_data_url(self, data, **kwargs):
        """
        Validates url, which must be docs.google.com
        :param data:
        :param kwargs:
        :return:
        """
        data_url = data.get('data_url')
        if not validate_url(url=data_url):
            raise ValidationError('Wrong URL entered')

    @validates_schema
    # pylint:disable=no-self-use
    def validate_rows(self, data, **kwargs):
        """
        Validates entered rows
        :param data:
        :param kwargs:
        :return:
        """
        from_row = data.get('from_row')
        to_row = data.get('to_row')
        if not from_row.isalnum() or not to_row.isalnum():
            raise ValidationError('Wrong symbols entered')
        if from_row.isnumeric() or to_row.isnumeric():
            raise ValidationError('Entered only row/rows without specific column')
        if not validate_row(from_row) or not validate_row(to_row):
            raise ValidationError('Wrong rows entered')
