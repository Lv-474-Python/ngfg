"""
Field_Range model
"""

from app import DB
from .abstract_model import AbstractModel


class FieldRange(AbstractModel):
    """
    FieldRange model class

    :param field_id: a field to which range restriction applies to
    "param range_id: a range restriction that is applied to the field
    """

    __table__ = "fields_range"

    field_id = DB.Column(DB.Integer, DB.ForeignKey('fields.id', ondelete='CASCADE'), unique=True, \
                         nullable=False)
    range_id = DB.Column(DB.Integer, DB.ForeignKey('ranges.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"FieldRange {self.id}, field: {self.field_id}, range: {self.range_id}"
