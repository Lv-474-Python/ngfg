"""
SettingsAutocomplete model
"""
from marshmallow import fields

from app import DB, MA
from .abstract_model import AbstractModel


class SettingAutocomplete(AbstractModel):
    """
    SettingAutocomplete model class
    :param data_url: url to file that stores all possible options
    :param sheet: page name in Google Sheets
    :param from_row: from which line to start getting data from Google Sheets
    :param to_row: to which line to end getting data from Google Sheets
    :param field_id:which field to apply these settings to
    """
    __tablename__ = 'settings_autocomplete'

    data_url = DB.Column(DB.Text, nullable=False)
    sheet = DB.Column(DB.Text, nullable=False)
    from_row = DB.Column(DB.String, nullable=True)
    to_row = DB.Column(DB.String, nullable=True)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'),
                         nullable=False)

    def __repr__(self):
        return (f"<SettingAutocomplete {self.id}, data_url - {self.data_url}', "
                f"sheet - {self.sheet}, from_row - {self.from_row}, "
                f"to_row - {self.to_row}, Field - {self.field.id}")


class SettingAutocompleteSchema(MA.Schema):
    """
    Setting autocomplete schema
    """

    class Meta:
        """
        Setting autocomplete schema meta
        """
        fields = ("data_url", "sheet", "from_row", "to_row")

    data_url = fields.Str(required=True)
    sheet = fields.Str(required=True)
    from_row = fields.Str(required=True)
    to_row = fields.Str(required=True)
