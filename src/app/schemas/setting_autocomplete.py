"""
SettingAutocomplete schemas
"""
from marshmallow import fields

from app import MA


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
