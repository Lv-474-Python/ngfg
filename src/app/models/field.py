"""
Field model
"""

from app import DB


class Field(DB.Model):
    """
    Field model class
    """

    __tablename__ = 'fields'
    __table_args__ = (
        DB.UniqueConstraint('name', 'owner_id', name='unique_name_owner'),
    )

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String, unique=False, nullable=False)
    owner_id = DB.Column(DB.Integer, DB.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    field_type = DB.Column(DB.SmallInteger, unique=False, nullable=False)

    def __init__(self, name, owner_id, field_type):
        """
        :param name: field short name
        :param owner_id: user that created field
        :param field_type: field type
        """
        self.name = name
        self.owner_id = owner_id
        self.field_type = field_type

    @staticmethod
    def create(name, owner_id, field_type):
        """
        method to create Field instance

        :param name:  field short name
        :param owner_id: user that created field
        :param field_type: field type
        """
        field = Field(name, owner_id, field_type)
        DB.session.add(field)
        DB.session.commit()
        return field
