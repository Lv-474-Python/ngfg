"""
Tests for a google doc url validator
"""

from app.helper.google_docs_url_validator import validate_url


def test_validate_url_valid():
    """
    Test for google doc validator validate_url()
    Test case for when a valid url has been provided
    """
    url = 'https://docs.google.com/spreadsheets/d/AbCde1'

    assert validate_url(url) is True


def test_validate_url_invalid_netloc():
    """
    Test for google doc validator validate_url()
    Test case for when a url is invalid because of a wrong netloc
    """
    url_invalid_netloc = 'https://invalid.netloc.com/spreadsheets/d/AbCde1'
    assert validate_url(url_invalid_netloc) is False


def test_validate_url_invalid_d_value():
    """
    Test for google doc validator validate_url()
    Test ase for when a url is invalid because of a wrong d_value
    """
    url_invalid_d_value = 'https://docs.google.com/spreadsheets/abc/AbCde1'
    assert validate_url(url_invalid_d_value) is False


def test_validate_url_non_google_doc():
    """
    Test for google doc validator validate_url()
    Test case for when a url is not a google doc url
    """
    url_not_a_google_doc = 'https://not-a-google-doc.com'
    assert validate_url(url_not_a_google_doc) is False