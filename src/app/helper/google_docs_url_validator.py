"""
Google docs url validation function
"""
from urllib.parse import urlparse


def validate_url(url):
    """
    Google docs url validator
    :param url:
    :return: True if url is from google docs
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc == 'docs.google.com')
