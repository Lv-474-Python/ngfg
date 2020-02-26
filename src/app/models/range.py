"""Range model"""

from marshmallow import fields
from app import DB, MA
from .abstract_model import AbstractModel


class Range(AbstractModel):
    """
    Range model class
    :param min - int | restrictions:
        number - min value;
        text - min char amount;
        option - min amount of choices;
    :param max - int | restrictions:
        number - max value;
        text - max char amount;
        option - max amount of choices;
    """
    __tablename__ = 'ranges'

    min = DB.Column(DB.Integer, nullable=True)
    max = DB.Column(DB.Integer, nullable=True)

    fields_range = DB.relationship('FieldRange', backref='range')

    def __repr__(self):
        return f'<Range ID {self.id}, min {self.min}, max {self.max}>'


class RangeSchema(MA.Schema):
    """
    Range schema
    """

    class Meta:
        """
        Range schema meta
        """
        fields = ("min", "max")

    min = fields.Integer(required=False)
    max = fields.Integer(required=False)
