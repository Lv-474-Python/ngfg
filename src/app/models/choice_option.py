"""
ChoiceOption model
"""

from app import DB

#TODO - import in __init__.py in /models
class ChoiceOption(DB.Model):
    """
    Field model class
    """

    __tablename__ = 'choice_options'
    __table_args__ = (
        DB.UniqueConstraint('fields_id', 'option_text', name='unique_fields_option_text'),
    )

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    # fields -> field зробити
    fields_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'))
    option_text = DB.Column(DB.Text, unique=False, nullable=False)
    # change to field_type
    # index - чи мені треба індекси

    def __init__(self, fields_id, option_text):
        #TODO - docstring
        self.fields_id = fields_id
        self.option_text = option_text

    @staticmethod
    def create(name, fields_id, option_text):
        #TODO - docstring
        choice_option = ChoiceOption(fields_id, option_text)
        DB.session.add(choice_option)
        DB.session.commit()
        return choice_option
