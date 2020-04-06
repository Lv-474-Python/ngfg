"""
Tests for a google sheet row validator
"""

from app.helper.row_validation import validate_row


def test_validate_row_valid():
    """
    Test for validate_row()
    Test case for when row has been specified correctly
    """
    row = 'AAA123'
    assert validate_row(row) is True


def test_validate_row_extra_letters():
    """
    Test for validate_row()
    Test case for when row parameter is invalid because of extra letters
    """
    row_extra_letters = 'AAAA123'
    assert validate_row(row_extra_letters) is False


def test_validate_row_non_empty_split():
    """
    Test for validate_row()
    Test case for when row parameter is invalid because of a non-empty string at the end after the split
    """
    row_non_empty_split = 'AAA123AAA'
    assert validate_row(row_non_empty_split) is False


def test_validate_row_extra_splits():
    """
    Test for validate_row()
    Test case for when row parameter is invalid because of extra symbols
    """
    row_extra_splits = 'AAA123AAA123'
    assert validate_row(row_extra_splits) is False
