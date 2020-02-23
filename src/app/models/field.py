"""
Field model
"""

from app import DB, MA
from .abstract_model import AbstractModel


class Field(AbstractModel):
    """
    Field model class

    :param name: short field name
    :param owner_id: id of user that created this field
    :param field_type: field type
    """

    __tablename__ = 'fields'
    __table_args__ = (
        DB.UniqueConstraint('name', 'owner_id', name='unique_name_owner'),
    )

    name = DB.Column(DB.String, unique=False, nullable=False)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    field_type = DB.Column(DB.SmallInteger, unique=False, nullable=False)
    is_strict = DB.Column(DB.Boolean, default=False)

    choice_options = DB.relationship('ChoiceOption', backref='field')
    shared_fields = DB.relationship('SharedField', backref='field')
    settings_autocomplete = DB.relationship('SettingAutocomplete', backref='field')
    fields_range = DB.relationship('FieldRange', backref='field')

    def __repr__(self):
        return (f'<Field {self.id}, name - {self.name}, '
                f'type - {self.field_type}, is_strict - {self.is_strict}>')

class FieldSchema(MA.Schema):
    """
    Form schema
    """

    class Meta:
        """
        Field schema meta
        """
        fields = (
        "owner_id", "name", "field_type", "is_strict")