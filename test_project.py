import pytest

from unittest.mock import patch

from project import get_action, print_groups, print_history, print_types, conversion_logic, converter, converter_temp, converter_time, converter_time_2args, converter_time_3args, manage_group, manage_type, add_temp_type, manage_aliases, change_base_unit
from unit_converter.data_manager import load_data
from unit_converter.data_models import DataStore, ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData


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


# TODO: Test 'get_action' function


# Test 'print_groups' function
def test_print_groups(data_store):
    assert print_groups(data_store) == "Groups: length, time, mass, temperature, volume, area, speed"


# Test 'print_history' function
def test_print_history(data_store):
    data_store.conversion_log = [
        {
            "date": "2025-09-20T18:39:27.743896",
            "unit_group": "length",
            "from_type": "meters",
            "to_type": "yards",
            "amount": 50000.123059,
            "result": 54680.799495844265
        }
    ]
    result = print_history(data_store)
    assert "50,000.12306 meters = 54,680.7995 yards (Group: length)" in result

def test_print_history_time(data_store):
    data_store.conversion_log = [
        {
            "date": "2025-09-23T09:39:56.914011",
            "unit_group": "time",
            "from_time": "minutes",
            "to_time": "seconds",
            "factor_time": 1.0,
            "result": 60.0
        },
        {
            "date": "2025-09-23T09:40:11.681262",
            "unit_group": "time",
            "from_time": "jan",
            "to_time": "dec",
            "factor_time": "days",
            "result": 365.0
        }
    ]
    result = print_history(data_store)
    assert "1.0 minutes = 60.0 seconds (Group: time)" in result
    assert "365.0 days between jan dec (Group: time)" in result

def test_print_history_empty(data_store):
    data_store.conversion_log = []
    assert print_history(data_store) == "Error: Conversion history is empty!"

def test_print_history_valid_limit(data_store):
    data_store.conversion_log = [
        {
            "date": "2025-09-20T18:39:27.743896",
            "unit_group": "length",
            "from_type": "meters",
            "to_type": "yards",
            "amount": 50000.123059,
            "result": 54680.799495844265
        },
        {
            "date": "2025-09-20T18:43:48.752476",
            "unit_group": "length",
            "from_type": "meters",
            "to_type": "yards",
            "amount": 10.99999,
            "result": 12.029735345581804
        }
    ]
    result = print_history(data_store, limit=1)
    assert "50,000.12306 meters = 54,680.7995 yards (Group: length)" in result
    assert "10.99999 meters = 12.02974 yards (Group: length)" not in result

def test_print_history_invalid_limit(data_store):
    data_store.conversion_log = [
        {
            "date": "2025-09-20T18:39:27.743896",
            "unit_group": "length",
            "from_type": "meters",
            "to_type": "yards",
            "amount": 50000.123059,
            "result": 54680.799495844265
        }
    ]
    assert print_history(data_store, limit="invalid") == "Error: 'limit' must be a number!"

def test_print_history_negative_limit(data_store):
    data_store.conversion_log = [
        {
            "date": "2025-09-20T18:39:27.743896",
            "unit_group": "length",
            "from_type": "meters",
            "to_type": "yards",
            "amount": 50000.123059,
            "result": 54680.799495844265
        }
    ]
    assert print_history(data_store, limit=-1) == "Error: 'limit' must be a positive number!"


# Test 'print_types' function
def test_print_types(data_store):
    assert print_types(data_store, "length") == "'length' units: meters ('m', 'meter', 'metre', 'metres'), centimeters ('cm', 'centimeter', 'centimetre', 'cetimetres'), millimeters ('mm', 'millimeter', 'millimetre', 'millimetres'), kilometers ('km', 'kilometer', 'kilometre', 'kilometres'), feet ('ft', 'foot'), inches ('in', 'inch'), yards ('yd', 'yds', 'yard'), miles ('mi', 'mile'), nautical_miles ('nmi', 'nm', 'nautical_mile')"

def test_types_print_invalid_group(data_store):
    assert print_types(data_store, "invalid") == "Error: 'invalid' is not a valid group!"

def test_print_types_get_input(data_store):
    with patch("project.get_users_input", return_value="length"):
        assert print_types(data_store) == "'length' units: meters ('m', 'meter', 'metre', 'metres'), centimeters ('cm', 'centimeter', 'centimetre', 'cetimetres'), millimeters ('mm', 'millimeter', 'millimetre', 'millimetres'), kilometers ('km', 'kilometer', 'kilometre', 'kilometres'), feet ('ft', 'foot'), inches ('in', 'inch'), yards ('yd', 'yds', 'yard'), miles ('mi', 'mile'), nautical_miles ('nmi', 'nm', 'nautical_mile')"

def test_print_types_get_input_empty_group(data_store):
    with patch("project.get_users_input", return_value=""):
        with pytest.raises(ValueError, match="Unit group cannot be empty!"):
            print_types(data_store)

def test_print_types_get_input_invalid_group(data_store):
    with patch("project.get_users_input", return_value="invalid"):
        with pytest.raises(KeyError, match="'invalid' is not a valid group!"):
            print_types(data_store)


# Test 'conversion_logic' function
def test_conversion_logic(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = "10"
    assert conversion_logic(data_store, conversion_data) == "10.0 meters = 10.93613 yards"

def test_conversion_logic_empty_group(data_store, conversion_data):
    conversion_data.unit_group = None
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = "10"
    with pytest.raises(ValueError, match="Unit group cannot be empty!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_group(data_store, conversion_data):
    conversion_data.unit_group = "invalid"
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = "10"
    with pytest.raises(KeyError, match="'invalid' is not a valid group!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_from_type(data_store, conversion_data):
    conversion_data.to_type = "yards"
    conversion_data.amount = "10"
    with pytest.raises(ValueError, match="'unit_type' cannot be empty!"):
        conversion_logic(data_store, conversion_data)   

def test_conversion_logic_invalid_from_type(data_store, conversion_data):
    conversion_data.from_type = "invalid"
    conversion_data.to_type = "yards"
    conversion_data.amount = "10"
    with pytest.raises(KeyError, match="Invalid unit type!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_to_type(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "invalid"
    conversion_data.amount = "10"
    with pytest.raises(ValueError, match="'unit_type' cannot be empty!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_to_type(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "invalid"
    conversion_data.amount = "10"
    with pytest.raises(KeyError, match="Invalid unit type!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_amount(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    with pytest.raises(ValueError, match="'amount' cannot be empty"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_amount(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = "invalid"
    with pytest.raises(ValueError, match="Invalid amount!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_temperature_negative_amount(data_store, conversion_data):
    conversion_data.unit_group = "temperature"
    conversion_data.from_type = "kelvin"
    conversion_data.to_type = "celsius"
    conversion_data.amount = "-10"
    with pytest.raises(ValueError, match="Kelvin temperature cannot be negative!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.time_input = "minutes seconds 1"
    assert conversion_logic(data_store, conversion_data) == "1.0 minutes = 60.0 seconds"

def test_conversion_logic_empty_time_input(data_store, conversion_data):
    conversion_data.unit_group = "time"
    with pytest.raises(ValueError, match="Time conversion can't be empty! Enter an expression!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_time_input(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.time_input = "invalid"
    with pytest.raises(ValueError, match="Incorrect format for time conversion!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_from_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.to_time = "seconds"
    conversion_data.factor_time = "10"
    with pytest.raises(ValueError, match="Enter a value to convert from!"):
        conversion_logic(data_store, conversion_data)
    
def test_conversion_logic_invalid_from_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.from_time = "invalid"
    conversion_data.to_time = "seconds"
    conversion_data.factor_time = "10"
    with pytest.raises(ValueError, match="'Invalid 'from_time': 'invalid'"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_to_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.from_time = "minutes"
    conversion_data.factor_time = "10"
    with pytest.raises(ValueError, match="Enter a value to convert to!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_to_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.from_time = "minutes"
    conversion_data.to_time = "invalid"
    conversion_data.factor_time = "10"
    with pytest.raises(ValueError, match="Invalid 'to_time'"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_empty_factor_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.from_time = "minutes"
    conversion_data.to_time = "seconds"
    with pytest.raises(ValueError, match="'factor_time' cannot be empty!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_invalid_factor_time(data_store, conversion_data):
    conversion_data.unit_group = "time"
    conversion_data.from_time = "minutes"
    conversion_data.to_time = "seconds"
    conversion_data.factor_time = "invalid"
    with pytest.raises(KeyError, match="Factor time 'invalid' not found in 'time' group!"):
        conversion_logic(data_store, conversion_data)

def test_conversion_logic_get_input(data_store):
    with patch("project.get_users_input", return_value="length"):
        with patch("project.get_users_input", return_value=("meters", "yards")):
            with patch("project.get_users_input", return_value="10"):
                assert conversion_logic(data_store) == "10.0 meters = 10.93613 yards"

def test_conversion_logic_get_input_time(data_store):
    with patch("project.get_users_input", return_value="length"):
        with patch("project.get_users_input", return_value=("minutes seconds 1")):
            assert conversion_logic(data_store) == "1.0 minutes = 60.0 seconds"


# Test 'converter' function
def test_converter(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = 10.0
    assert converter(data_store, conversion_data) == 10.936132983377078

def test_converter_temperature(data_store, conversion_data):
    conversion_data.unit_group = "temperature"
    conversion_data.from_type = "celsius"
    conversion_data.to_type = "kelvin"
    conversion_data.amount = 10.0
    assert converter(data_store, conversion_data) == 283.15

def test_converter_zero_division(data_store, conversion_data):
    conversion_data.from_type = "meters"
    conversion_data.to_type = "yards"
    conversion_data.amount = 10.0
    data_store.units["length"]["yard"] = 0
    with pytest.raisse(ZeroDivisionError, match="Can't Divide by zero"):
        converter(data_store, conversion_data)


# Test 'converter_temp' function
def test_converter_temp(data_store, conversion_data):
    conversion_data.unit_group = "temperature"
    conversion_data.from_type = "celsius"
    conversion_data.to_type = "kelvin"
    conversion_data.amount = 10.0
    assert converter_temp(data_store, conversion_data) == 283.15

def test_converter_temp_zero_division(data_store, conversion_data):
    conversion_data.unit_group = "temperature"
    conversion_data.from_type = "celsius"
    conversion_data.to_type = "kelvin"
    conversion_data.amount = 10.0
    data_store.units["temperature"]["celius"] = [0.0, 273.15]
    with pytest.raises(ZeroDivisionError, match="Can't Divide by zero"):
        converter_temp(data_store, conversion_data)


# Test 'converter_time' function