import pytest

from unittest.mock import patch

from unit_converter.data_manager import load_data
from unit_converter.data_models import DataStore, ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData, validate_for_history, validate_args_number


# Setup DataStore to be used on all tests that require DataStore
@pytest.fixture
def data_store():
    return DataStore(*load_data())

# Setup fixtures to be used on their respective class tests
@pytest.fixture
def conversion_data():
    return ConversionData(unit_group="length")

@pytest.fixture
def manage_group_data():
    return ManageGroupData(unit_group="length")

@pytest.fixture
def manage_type_data():
    return ManageTypeData(unit_group="length")

@pytest.fixture
def aliases_data():
    return AliasesData(unit_group="length")

@pytest.fixture
def change_base_data():
    return ChangeBaseData(unit_group="length")


# Test 'ConversionData' class methods


# Test 'ManageGroupData' class methods


# Test 'ManageTypeData' class methods


# Test 'AliasesData' class methods
def test_validate_unit_type_valid(data_store, aliases_data):
    aliases_data.unit_type = 'meters'
    aliases_data.validate_unit_type(data_store)

def test_validate_unit_type_empty_type(data_store, aliases_data):
    with pytest.raises(KeyError, match="'None'  is not a valid unit type for 'length' group!"):
        aliases_data.validate_unit_type(data_store)

def test_validate_action_valid(aliases_data):
    aliases_data.action = "add"
    aliases_data.validate_action()

def test_validate_action_empty(aliases_data):
    with pytest.raises(ValueError, match="'action' cannot be empty!"):
        aliases_data.validate_action()

def test_validate_action_invalid(aliases_data):
    aliases_data.action = "invalid"
    with pytest.raises(ValueError, match="Invalid action: 'invalid'"):
        aliases_data.validate_action()

def test_validate_alias_valid_add(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "mtr"
    aliases_data.validate_alias(data_store)

def test_validate_alias_valid_remove(data_store, aliases_data):
    aliases_data.action = "remove"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "m"
    aliases_data.validate_alias(data_store)

def test_validate_alias_empty(data_store, aliases_data):
    with pytest.raises(ValueError, match="Alias cannot be empty!"):
        aliases_data.validate_alias(data_store)

def test_validate_alias_already_alias(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "m"
    with pytest.raises(ValueError, match=f"'m' is already being used as an alias in 'length'!"):
        aliases_data.validate_alias(data_store)

def test_validate_alias_already_unit_group(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "length"
    with pytest.raises(KeyError, match="'length' is already being used to name an unit group!"):
        aliases_data.validate_alias(data_store)

def test_validate_alias_already_unit_type(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "meters"
    with pytest.raises(KeyError, match="'meters' is already being used as an unit type in 'length' group!"):
        aliases_data.validate_alias(data_store)

def test_validate_alias_no_alias_in_group(data_store, aliases_data):
    aliases_data.action = "remove"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "invalid"
    with pytest.raises(ValueError, match="'invalid' is not an alias of 'length' group"):
        aliases_data.validate_alias(data_store)

def test_validate_alias_no_alias_in_type(data_store, aliases_data):
    aliases_data.action = "remove"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "km"
    with pytest.raises(ValueError, match="'invalid' is not an alias for 'meters'"):
        aliases_data.validate_alias(data_store)

def test_validate_for_aliases_valid_alias(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "meters"
    aliases_data.alias = "m"
    aliases_data.validate_for_aliases(data_store)
    assert aliases_data.unit_type == "meters"

def test_validate_for_aliases_invalid_type(data_store, aliases_data):
    aliases_data.action = "add"
    aliases_data.unit_type = "invalid"
    aliases_data.alias = "m"
    with pytest.raises(ValueError, match="'invalid' is not an alias of 'length' group"):
        aliases_data.validate_for_aliases(data_store)


# Test 'ChangeBaseData' class methods
def test_validate_for_change_base_valid(data_store, change_base_data):
    change_base_data.new_base_unit = "mile"
    change_base_data.validate_for_change_base(data_store)

def test_validate_for_change_base_empty_type(data_store, change_base_data):
    with pytest.raises(ValueError, match="Unit type cannot be empty!"):
        change_base_data.validate_for_change_base(data_store)

def test_validate_for_change_base_wrong_group(data_store, change_base_data):
    change_base_data.new_base_unit = "invalid"
    with pytest.raises(KeyError, match="'invalid' is not an unit type for 'length' group"):
        change_base_data.validate_for_change_base(data_store)

def test_validate_for_change_base_already_base(data_store, change_base_data):
    change_base_data.new_base_unit = data_store.base_units["length"]
    with pytest.raises(ValueError, match=f"'{change_base_data.new_base_unit}' is already the current base unit for 'length' group"):
        change_base_data.validate_for_change_base(data_store)


# Test 'validate_for_history' function
def test_validate_for_history_empty(data_store):
    data_store.conversion_log = []
    with pytest.raises(ValueError, match="Conversion history is empty!"):
        validate_for_history(data_store, limit=10)

def test_validate_for_history_invalid_limit(data_store):
    with pytest.raises(ValueError, match="'limit' must be a number!"):
        validate_for_history(data_store, limit="invalid")

def test_validate_for_history_negative_limit(data_store):
    with pytest.raises(ValueError, match="'limit' must be a positive number!"):
        validate_for_history(data_store, limit=-10)


# Test 'validate_args_number' function
def test_validate_args_number_valid():
    validate_args_number(command="test")

def test_validate_args_number_args():
    with pytest.raises(TypeError, match="Too many positional arguments for 'command' command!"):
        validate_args_number("extra", command="command")

def test_validate_args_number_kwargs():
    with pytest.raises(TypeError, match="Unexpected keyword argument for 'command' command!"):
        validate_args_number(command="command", extra="extra")