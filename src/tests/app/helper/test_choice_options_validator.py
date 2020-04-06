"""
Module to test choice options validator
"""

import pytest
from app.helper.choice_options_validator import (
    check_for_repeated_options,
    check_for_same_options,
    validate_repeats_of_choice_options,
)
from .helper_test_data import (
    CHOICE_OPTIONS_VALIDATOR_CHECK_REPEATED_OPTIONS,
    CHOICE_OPTIONS_VALIDATOR_CHECK_SAME_OPTIONS,
    CHOICE_OPTIONS_VALIDATOR_VALIDATE_REPEATS
)


@pytest.mark.parametrize("test_input, expected", CHOICE_OPTIONS_VALIDATOR_CHECK_REPEATED_OPTIONS)
def test_check_for_repeated_options(test_input, expected):
    result = check_for_repeated_options(test_input)
    assert result == expected


@pytest.mark.parametrize("test_input, expected", CHOICE_OPTIONS_VALIDATOR_CHECK_SAME_OPTIONS)
def test_check_for_same_options(test_input, expected):
    added, removed = test_input
    result = check_for_same_options(added, removed)
    assert result == expected


@pytest.mark.parametrize("test_input, expected", CHOICE_OPTIONS_VALIDATOR_VALIDATE_REPEATS)
def test_validated_repeats_of_choice_options(test_input, expected):
    added, removed = test_input
    result = validate_repeats_of_choice_options(added, removed)
    assert result == expected
