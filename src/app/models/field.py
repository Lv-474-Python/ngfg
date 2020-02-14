"""
Field model
"""

from app import DB

#TODO - import in __init__.py in /models
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
    type = DB.Column(DB.SmallInteger, unique=False, nullable=True)

    # change to field_type
    # index - чи мені треба індекси

    def __init__(self, name, owner_id=None, type=None):
        #TODO - docstring
        self.name = name
        self.owner_id = owner_id
        self.type = type

    @staticmethod
    def create(name, owner_id, type):
        #TODO - docstring
        field = Field(name, owner_id, type)
        DB.session.add(field)
        DB.session.commit()
        return field
