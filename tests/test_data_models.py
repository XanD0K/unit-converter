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
def test_validate_from_type_valid(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.validate_from_type(data_store)

def test_validate_from_type_empty(data_store, conversion_data):
    with pytest.raises(ValueError, match="'unit_type' cannot be empty!"):
        conversion_data.validate_from_type(data_store)

def test_validate_from_type_invalid(data_store, conversion_data):
    conversion_data.from_type = "invalid"
    with pytest.raises(KeyError, match="Invalid unit type!"):
        conversion_data.validate_from_type(data_store)

def test_validate_to_type_valid(data_store, conversion_data):
    conversion_data.to_type = "meters"
    conversion_data.validate_to_type(data_store)

def test_validate_to_type_empty(data_store, conversion_data):
    with pytest.raises(ValueError, match="'unit_type' cannot be empty!"):
        conversion_data.validate_to_type(data_store)

def test_validate_to_type_invalid(data_store, conversion_data):
    conversion_data.to_type = "invalid"
    with pytest.raises(KeyError, match="Invalid unit type!"):
        conversion_data.validate_to_type(data_store)

def test_validate_amount_valid(conversion_data):
    conversion_data.amount = "10"
    conversion_data.validate_amount()
    assert conversion_data.amount = 10.0

def test_validate_amount_empty(conversion_data):
    with pytest.raises(ValueError, match="'amount' cannot be empty"):
        conversion_data.validate_amount()

def test_validate_amount_invalid(conversion_data):
    conversion_data.amount = "invalid"
    with pytest.raises(ValueError, match="Invalid amount!"):
        conversion_data.validate_amount()

def test_validate_amount_negative_kelvin(conversion_data):
    conversion_data.unit_group = "kelvin"
    conversion_data.amount = "-10"
    with pytest.raises(ValueError, match="Kelvin temperature cannot be negative!"):
        conversion_data.validate_amount()

def test_validate_time_input_valid(conversion_data):


# Test 'ManageGroupData' class methods
def test_validate_action_valid(manage_group_data):
    manage_group_data.action = "add"
    manage_group_data.validate_action()

def test_validate_action_empty(manage_group_data):
    with pytest.raises(ValueError, match="'action' cannot be empty!"):
        manage_group_data.validate_action()

def test_validate_action_invalid(manage_group_data):
    manage_group_data.action = "invalid"
    with pytest.raises(ValueError, match="Invalid action: 'invalid'"):
        manage_group_data.validate_action()

def test_validate_add_action_valid(data_store, manage_group_data):
    manage_group_data.unit_group = "new_group"
    manage_group_data.validate_add_action(data_store)

def test_validate_add_action_already_group(data_store, manage_group_data):
    with pytest.raises(KeyError, match="'length' is already an existed group!")
        manage_group_data.validate_add_action(data_store)

def test_validate_remove_action_valid(data_store, manage_group_data):
    manage_group_data.validate_remove_action(data_store)

def test_validate_remove_action_invalid_type(data_store, manage_group_data):
    manage_group_data.unit_group = "invalid"
    with pytest.raises(KeyError, match="'invalid' is not a valid group!"):
        manage_group_data.validate_remove_action(data_store)

def test_validate_new_base_unit_valid(data_store, manage_group_data):
    manage_group_data.unit_group = "new_group"
    manage_group_data.new_base_unit = "new_base_unit"
    validate_new_base_unit(data_store)
    assert manage_group_data.unit_group = "new_group"
    assert manage_group_data.new_base_unit = "new_base_unit"

def test_validate_new_base_unit_empty(data_store, manage_group_data):
    with pytest.raises(ValueError, match="'new_base_unit' cannot be empty"):
        manage_group_data.validate_new_base_unit(data_store)

def test_validate_new_base_unit_already_group(data_store, manage_group_data):
    manage_group_data.new_base_unit = "length"
    with pytest.raises(KeyError, match="'{self.new_base_unit}' is already an unit group name!"):
        manage_group_data.validate_new_base_unit(data_store)

def test_validate_new_base_unit_same_name(data_store, manage_group_data):
    manage_group_data.unit_group = "new_group"
    manage_group_data.new_base_unit = "new_group"
    with pytest.raises(ValueError, match="'new_base_unit' can't have the same name as 'unit_group'"):
        manage_group_data.validate_new_base_unit(data_store)

def test_validate_for_manage_group():


# Test 'ManageTypeData' class methods
def test_validate_action_valid(manage_type_data):
    aliases_data.action = "add"
    aliases_data.validate_action()

def test_validate_action_empty(manage_type_data):
    with pytest.raises(ValueError, match="'action' cannot be empty!"):
        aliases_data.validate_action()

def test_validate_action_invalid(manage_type_data):
    aliases_data.action = "invalid"
    with pytest.raises(ValueError, match="Invalid action: 'invalid'"):
        aliases_data.validate_action()

def test_validate_add_action_valid(data_store, manage_type_data):
    manage_type_data.unit_type = "new_type"
    manage_type_data.validate_add_action(data_store)

def test_validate_add_action_empty_type(data_store, manage_type_data):
    with pytest.raises(ValueError, match="You can't leave that field empty!"):
        manage_type_data.validate_add_action(data_store)

def test_validate_add_action_already_group(data_store, manage_type_data):
    manage_type_data.unit_type = "length"
    with pytest.raises(KeyError, match="'length' is already an unit group name!"):
        manage_type_data.validate_add_action(data_store)

def test_validate_add_action_already_type(data_store, manage_type_data):
    manage_type_data.unit_type = "meters"
    with pytest.raises(ValueError, match="'meters' is already an unit type in 'length' group!"):
        manage_type_data.validate_add_action(data_store)

def test_validate_add_action_already_alias(data_store, manage_type_data):
    manage_type_data.unit_type = "m"
    with pytest.raises(ValueError, match="'m' is already being used as an alias in 'length' group"):
        manage_type_data.validate_add_action(data_store)

def test_validate_remove_action_valid(data_store, manage_type_data):
    manage_type_data.unit_type = "mile"
    manage_type_data.validate_remove_action(data_store)

def test_validate_remove_action_empty_type(data_store, manage_type_data):
    with pytest.raises(ValueError, match="You can't leave that field empty!"):
        manage_type_data.validate_remove_action(data_store)

def test_validate_remove_action_invalid_type(data_store, manage_type_data):
    manage_type_data.unit_type = "invalid"
    with pytest.raises(ValueError, match="'invalid' is not an unit type in 'length' group!"):
        manage_type_data.validate_remove_action(data_store)

def test_validate_remove_action_already_base(data_store, manage_type_data):
    manage_type_data.unit_type = data_store.base_units["length"]
    with pytest.raises(ValueError, match= "Cannot remove base unit!"):
        manage_type_data.validate_remove_action(data_store)

def test_validate_value_valid(manage_type_data):
    manage_type_data.value = "10"
    manage_type_data.validate_value()
    assert manage_type_data.value == 10.0

def test_validate_value_empty(manage_type_data):
    with pytest.raises(ValueError, match="'value' cannot be empty!"):
        manage_type_data.validate_value()

def test_validate_value_invalid(manage_type_data):
    manage_type_data.value = "invalid"
    with pytest.raises(ValueError, match="Invalid conversion factor!"):
        manage_type_data.validate_value()

def test_validate_factor_valid(manage_type_data):
    manage_type_data.factor = "10"
    manage_type_data.validate_factor()
    assert manage_type_data.factor == 10.0

def test_validate_factor_empty(manage_type_data):
    with pytest.raises(ValueError, match="'factor' cannot be empty!"):
        manage_type_data.validate_factor()

def test_validate_factor_invalid(manage_type_data):
    manage_type_data.factor = "invalid"
    with pytest.raises(ValueError, match="Invalid conversion factor!"):
        manage_type_data.validate_factor()

def test_validate_factor_negative(manage_type_data):
    manage_type_data.factor = -10
    with pytest.raises(ValueError, match="Conversion factor must be positive!"):
        manage_type_data.validate_factor()

def test_validate_offset_valid(manage_type_data):
    manage_type_data.offset = "10"
    manage_type_data.validate_offset()
    assert manage_type_data.offset == 10.0

def test_validate_offset_empty(manage_type_data):
    with pytest.raises(ValueError, match="'offset' cannot be empty!"):
        manage_type_data.validate_offset()

def test_validate_offset_invalid(manage_type_data):
    manage_type_data.offset = "invalid"
    with pytest.raises(ValueError, match="Invalid conversion offset!"):
        manage_type_data.validate_offset()

def test_validate_for_manage_type_add_valid(data_store, manage_type_data):


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