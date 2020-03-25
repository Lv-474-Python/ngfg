import pytest
from app.helper.answer_validation import is_numeric

def test_is_numeric_true():
    data = 1
    assert is_numeric(data) == True

def test_is_numeric_false():
    data = [1]
    assert is_numeric(data) == False