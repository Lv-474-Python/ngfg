"""
Range schemas
"""
from marshmallow import fields, validates_schema, ValidationError

from app import MA
from app.helper.constants import MIN_POSTGRES_INT, MAX_POSTGRES_INT


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
