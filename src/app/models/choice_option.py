"""
ChoiceOption model
"""

from app import DB

class ChoiceOption(DB.Model):
    """
    ChoiceOption model class
    """

    __tablename__ = 'choice_options'
    __table_args__ = (
        DB.UniqueConstraint('field_id', 'option_text', name='unique_field_option_text'),
    )

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'))
    option_text = DB.Column(DB.Text, unique=False, nullable=False)

    def __init__(self, field_id, option_text):
        """
        :param field_id: field that has this 
        :param option_text: 
        """
        self.field_id = field_id
        self.option_text = option_text

    # @staticmethod
    # def create(name, field_id, option_text):
    #     #TODO - docstring
    #     choice_option = ChoiceOption(field_id, option_text)
    #     DB.session.add(choice_option)
    #     DB.session.commit()
    #     return choice_option
