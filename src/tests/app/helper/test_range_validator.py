"""
Module to test range validator
"""

import pytest
from app.helper.range_validator import validate_range_checkbox, validate_range_text
from .helper_test_data import (
    RANGE_VALIDATOR_VALIDATE_CHECKBOX,
    RANGE_VALIDATOR_VALIDATE_TEXT
)


@pytest.mark.parametrize("test_input, expected", RANGE_VALIDATOR_VALIDATE_CHECKBOX)
def test_validate_range_checkbox(test_input, expected):
    range_min, range_max = test_input
    errors = validate_range_checkbox(range_min=range_min, range_max=range_max)
    assert errors == expected


@pytest.mark.parametrize("test_input, expected", RANGE_VALIDATOR_VALIDATE_TEXT)
def test_validate_range_text(test_input, expected):
    range_min, range_max = test_input
    errors = validate_range_text(range_min=range_min, range_max=range_max)
    assert errors == expected
