import json
import sys

from datetime import datetime, timedelta
from fractions import Fraction
from pathlib import Path

from unit_converter.data_models import DataStore


# Creates path to "final-project" directory
BASE_DIR = Path(__file__).parent.parent


def load_data():
    """Imports all '.json' files which handles data management"""
    # Opens dictionary with all units available
    with open(BASE_DIR / "data" / "units.json", "r") as file:
        units = json.load(file)
    # Opens dictionary of base units for each group
    with open(BASE_DIR / "data" / "base_units.json", "r") as file:
        base_units = json.load(file)
    # Opens dictionary containing all conversions history
    with open(BASE_DIR / "data" / "conversion_log.json", "r") as file:
        conversion_log = json.load(file)
    # Opens dictionary that contains all aliases for each unit type
    with open(BASE_DIR / "data" / "unit_aliases.json", "r") as file:
        unit_aliases = json.load(file)
    with open(BASE_DIR / "data" / "month_days.json", "r") as file:
        month_days = json.load(file)
    with open(BASE_DIR / "data" / "original_units.json", "r") as file:
        original_units = json.load(file)

    validate_data(units, base_units, conversion_log, unit_aliases, month_days, original_units)
    return units, base_units, conversion_log, unit_aliases, month_days, original_units 


def validate_data(units, base_units, conversion_log, unit_aliases, month_days, original_units):
    """Validates dictionaries before entering the program"""
    # Ensures 'units.json' is a dictionary and it's not empty
    if not isinstance(units, dict) or not units:
        raise ValueError("'units.json' structure is corrupted!")
    # Ensures 'base_units.json' is a dictionary and it's not empty
    if not isinstance(base_units, dict) or not base_units:
        raise ValueError("'base_units.json' structure is corrupted!")
    for unit_group in units:
        # Ensures every unit group in 'units.json' is also a dictionary
        if not isinstance(units[unit_group], dict):
            raise ValueError(f"'units.json' is corrupted! Its '{units[unit_group]}' key should also be a dictionary!")
        # Ensures every group in 'units.json' is also a group in 'base_units.json'
        if unit_group not in base_units:
            raise KeyError(f"Dictionaries don't match! '{unit_group}' should also be a key in 'base_units.json'!")
        # Ensures base unit for each group is correctly define in 'units.json'
        if base_units[unit_group] not in units[unit_group]:
            raise KeyError(f"The base unit '{base_units[unit_group]}' for {unit_group} group is not present on 'units.json'!")
    # Ensures 'conversion_log' is a list
    if not isinstance(conversion_log, list):
        raise ValueError("'convert_history' structure is corrupted!")
    # Ensures 'month_days' is a dictionary and it's not empty
    if not isinstance(month_days, dict) or not month_days:
        raise ValueError("'month_days' structure is corrupted!")
    # Ensures 'unit_aliases' is a dictionary and it's not empty
    if not isinstance(unit_aliases, dict) or not unit_aliases:
        raise ValueError("'unit_aliases.json' structure is corrupted!")
    for unit_group in unit_aliases:
        if unit_group not in units:
            raise KeyError(f"Dictionaries don't match! '{unit_group}' should also be a key in 'units.json' dictionary!")
        # Ensures every unit group in 'unit_aliases.json' is also a dictionary
        if not isinstance(unit_aliases[unit_group], dict):
            raise ValueError(f"'unit_aliases.json' is corrupted! Its '{unit_aliases[unit_group]}' key should also be a dictionary!")
        # Ensures no duplicate aliases in the same unit group
        seen_aliases = set()
        for alias in unit_aliases[unit_group]:
            if alias in seen_aliases:
                raise ValueError(f"'unit_aliases.json' is corrupted! There are duplicate aliases in '{unit_aliases[unit_group]}' group !")
            seen_aliases.add(alias)
    # Ensures 'original_units.json' is a dictionary and it's not empty
    if not isinstance(original_units, dict) or not original_units:
        raise ValueError("'original_units.json' structure is corrupted!")
    for unit_group in original_units:
        # Ensures every unit group in 'original_units.json' is also a dictionary
        if not isinstance(original_units[unit_group], dict):
            raise ValueError(f"'units.json' is corrupted! Its '{original_units[unit_group]}' key should also be a dictionary!")
        # Ensures every group in 'original_units.json' is also a group in 'base_units.json'
        if unit_group not in base_units:
            raise KeyError(f"Dictionaries don't match! '{unit_group}' should also be a key in 'base_units.json'!")
        # Ensures base unit for each group is correctly define in 'original_units.json'
        if base_units[unit_group] not in original_units[unit_group]:
            raise KeyError(f"The base unit '{base_units[unit_group]}' for {unit_group} group is not present on 'units.json'!")
        for unit_type in original_units[unit_group]:
            if unit_type not in units[unit_group]:
                raise KeyError(f"The unit_type '{unit_type}' should also be an unit_type in 'units.json'!")
 


def add_to_log(data, unit_data, is_time_convertion=False) -> None:
    """Adds successfully converted value to log file (conversion_log.json)"""
    unit_group = unit_data.unit_group

    if is_time_convertion:
        from_time = unit_data.from_time
        to_time = unit_data.to_time
        factor_time = unit_data.factor_time
        new_time = unit_data.new_time
        if all(x is None for x in (from_time, to_time, factor_time, new_time)):
            raise ValueError("Missing required arguments!")
        entry = {
            "date": datetime.now().isoformat(),
            "unit_group": unit_group,
            "from_time": from_time,
            "to_time": to_time,
            "factor_time": factor_time,
            "result": float(new_time)
        }
    else:
        from_type = unit_data.from_type
        to_type = unit_data.to_type
        amount = unit_data.amount
        new_value = unit_data.new_value
        if all(x is None for x in (from_type, to_type, amount, new_value)):
            raise ValueError("Missing required arguments!")
        entry = {
            "date": datetime.now().isoformat(),
            "unit_group": unit_group,
            "from_type": from_type,
            "to_type": to_type,
            "amount": amount,
            "result": float(new_value)
        }

    # Cleans 'conversion_log.json' file, preventing big files
    data.conversion_log = clean_history(data)
    # Appends new entry
    data.conversion_log.append(entry)

    save_data(data.conversion_log, "conversion_log")


def clean_history(data):
    """Cleans 'conversion_log.json' file keeping only entries not older than 3 days"""
    return [entry for entry in data.conversion_log if "date" in entry and datetime.now() - datetime.fromisoformat(entry["date"]) <= timedelta(days=3)]


def save_data(data, file_name):
    """Tries saving the modifications in the '.json' file, or return its backup"""
    try:
        backup = data.copy()
        with open(BASE_DIR / "data" / f"{file_name}.json", "w") as file:
            json.dump(data, file, indent=4)
    except PermissionError:
        print(f"Error! You don't have permition to write to {file_name}!")        
        return backup
    return data


def refactor_value(data, unit_group, new_base_unit):
    """Refactor all values for 'chage-base' action"""
    if unit_group == "temperature":
        new_base_factor, new_base_offset = data.original_units[unit_group][new_base_unit]
        zero_division_checker(new_base_factor)            
        for unit_type in data.original_units[unit_group]:
            factor, offset = data.original_units[unit_group][unit_type]
            factor /= new_base_factor
            offset -= new_base_offset
            data.units[unit_group][unit_type] = [factor, offset]
    else:
        new_base_factor = data.original_units[unit_group][new_base_unit]
        zero_division_checker(new_base_factor)        
        for unit_type in data.original_units[unit_group]:
            value = data.original_units[unit_group][unit_type] / new_base_factor
            data.units[unit_group][unit_type] = value
    return


def zero_division_checker(num):
    """Prevents division by zero"""
    if num == 0:
        raise ZeroDivisionError("Can't Divide by zero")