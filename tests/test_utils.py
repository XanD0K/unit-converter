import pytest
import sys

from unittest.mock import patch

from unit_converter.utils import get_users_input, get_unit_group, validate_unit_group
from unit_converter.data_manager import load_data
from unit_converter.data_models import DataStore, ConversionData

# Setup DataStore to be used on all tests
@pytest.fixture
def data_store():
    return DataStore(*load_data())

# Setup ConversionData to be used on all tests
@pytest.fixture
def conversion_data():
    return ConversionData(
        unit_group="length"
    )

# Tests 'get_users_input' function
def test_get_users_input_str():
    with patch("builtins.input", return_value="Hello"):
        assert get_users_input("Input: ") == "hello"

def test_get_users_input_whitespace():
    with patch("builtins.input", return_value="  white space  "):
        assert get_users_input("Input: ") == "white space"

def test_get_users_input_empty():
    with patch("builtins.input", return_value=""):
        assert get_users_input("Input: ") == ""

def test_get_users_input_quit():
    with patch("builtins.input", return_value="quit"):
        with pytest.raises(SystemExit) as error:
            get_users_input("Input: ")
        assert error.value.code == 0


# Tests 'get_unit_group' function
def test_get_unit_group_valid(data_store):
    with patch("unit_converter.utils.get_users_input", return_value=" Length "):
        result = get_unit_group(data_store)
        assert result == "length"

def test_get_unit_group_empty(data_store):
    with patch("unit_converter.utils.get_users_input", return_value=""):
        with pytest.raises(ValueError, match="Unit group cannot be empty!"):
            get_unit_group(data_store)

def test_get_unit_group_invalid(data_store):
    with patch("unit_converter.utils.get_users_input", return_value="lengthhh"):
        with pytest.raises(KeyError, match="'lengthhh' is not a valid group!"):
            get_unit_group(data_store)


# Tests 'validate_unit_group' function
def test_validate_unit_group_valid(data_store):
    validate_unit_group("length", data_store)

def test_validate_unit_group_empty(data_store):
    with pytest.raises(ValueError, match="Unit group cannot be empty!"):
            validate_unit_group("", data_store)

def test_validate_unit_group_invalid(data_store):
    with pytest.raises(KeyError, match="'lengthhh' is not a valid group!"):
            validate_unit_group("lengthhh", data_store)