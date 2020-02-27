"""Range model"""

from marshmallow import fields, validates_schema, ValidationError

from app import DB, MA
from app.helper.constants import MIN_POSTGRES_INT, MAX_POSTGRES_INT
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

    @validates_schema
    # pylint:disable=no-self-use
    def validate_range(self, data, **kwargs):
        """
        Validates range

        :param data:
        :param kwargs:
        :return:
        """
        min_value, max_value = data.get('min'), data.get('max')
        if min_value and not MIN_POSTGRES_INT < min_value < MAX_POSTGRES_INT:
            raise ValidationError(f'min must be between {MIN_POSTGRES_INT} and {MAX_POSTGRES_INT}')
        if max_value and not MIN_POSTGRES_INT < max_value < MAX_POSTGRES_INT:
            raise ValidationError(f'max must be between {MIN_POSTGRES_INT} and {MAX_POSTGRES_INT}')
        if (min_value and max_value) and min_value > max_value:
            raise ValidationError('min must be less than max')
