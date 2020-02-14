"""
Project enums
"""

import enum


class FieldType(enum.Enum):
    """
    Field types
    """
    Number = 1
    Text = 2
    TextArea = 3
    Radio = 4
    Autocomplete = 5
    Checkbox = 6
