import argparse
import json
import sys

from datetime import datetime, timedelta
from math import fabs

from unit_converter.data_manager import load_data, add_to_log, refactor_value, save_data, zero_division_checker
from unit_converter.data_models import ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData
from unit_converter.utils import print_introductory_messages, print_time_instructions, get_users_input, validate_unit_group, get_converter_units, get_amount, resolve_aliases, parse_time_input, parse_date_input, get_seconds, format_value, calculate_leap_years, validate_date, get_days_from_month, get_index_from_month, gets_days_from_index


def main() -> None:
    # Handles data loading and validation
    try:
        # Initiates a 'DataStore' object
        data = load_data()
    except (ValueError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Handles command-line arguments
    try:
        if len(sys.argv) > 1:
            handle_cli(sys.argv, data)
            sys.exit(0)  # Exits program after command-line execution
    except (ValueError, KeyError, ZeroDivisionError, TypeError) as e:
        print(f"Error: {e}")
        sys.exit(1) # Exits the program if any error happens
    print_introductory_messages()
    get_action(data)


def handle_cli(args, data):
    """Handles command-line interface (CLI)"""
    # Creates a copy of all command-line arguments
    formatted_args = args[:]

    # Adds description to program
    parser = argparse.ArgumentParser(prog="Unit Converter", description="Convert multiple types of units")
    
    # Defines subparser to handle multiple commands
    subparser = parser.add_subparsers(dest="command", help="Available commands")
    # 'groups' command
    subparser.add_parser("groups", aliases=["g"], help="List all unit groups")
    # 'history' command
    history_parser = subparser.add_parser("history", aliases=["h"], help="List conversion history (default=10)")
    history_parser.add_argument("--limit", "-l", type=int, default=10, help="Number entries to be printed")
    # 'types' command
    types_parser = subparser.add_parser("types", aliases=["t"], help="List all unit types in a group")
    types_parser.add_argument("unit_group", help="Unit group")
    # 'convert' command 
    convert_parser = subparser.add_parser("convert", aliases=["c"], help="Convert values")
    convert_parser.add_argument("unit_group", help="Unit group")
    convert_parser.add_argument("args", nargs="+", help="Source unit type")
    # 'manage-group' command
    manage_group_parser = subparser.add_parser("manage-group", aliases=["mg"], help="Add new unit group")
    manage_group_parser.add_argument("unit_group", help="Unit group")
    manage_group_parser.add_argument("action", choices=["add", "remove"], help="Action to perform")
    manage_group_parser.add_argument("new_base_unit", nargs="?", help="New base unit")
    # 'manage-type' command
    manage_type_parser = subparser.add_parser("manage-type", aliases=["mt"], help="Add new unit type")
    manage_type_parser.add_argument("unit_group", help="Unit group")
    manage_type_parser.add_argument("unit_type", help="Unit type to be added")
    manage_type_parser.add_argument("action", choices=["add", "remove"], help="Action to perform")
    manage_type_parser.add_argument("value", nargs="?", help="Conversion factor to base unit (not used for temperature)")
    manage_type_parser.add_argument("--factor", type=float, help="Conversion factor to temperature's base unit")
    manage_type_parser.add_argument("--offset", type=float, help="Offset to temperature")
    # 'aliases' command
    aliases_parser = subparser.add_parser("aliases", aliases=["a"], help="Manage unit's aliases")
    aliases_parser.add_argument("unit_group", help="Unit group")
    aliases_parser.add_argument("unit_type", help="Unit type")
    aliases_parser.add_argument("action", choices=["add", "remove"], help="Action to perform")
    aliases_parser.add_argument("alias", help="Alias used to add/remove to/from an unit")
    # 'change-base' command
    change_base_parser = subparser.add_parser("change-base", aliases=["cb"], help="Change unit base for a group")
    change_base_parser.add_argument("unit_group", help="Unit group")
    change_base_parser.add_argument("new_base_unit", help="New base unit")

    # Parses arguments and calls its respective function
    parsed_args = parser.parse_args(formatted_args[1:])  # Skips first argument (program's name)
    
    if parsed_args.command in ["groups", "g"]:
        print_groups(data)
    elif parsed_args.command in ["history", "h"]:
        print_history(data, parsed_args.limit)
    elif parsed_args.command in ["types", "t"]:
        unit_group = parsed_args.unit_group.lower()
        validate_unit_group(unit_group, data)
        print_types(data, unit_group)
    elif parsed_args.command in ["convert", "c"]:
        validate_unit_group(parsed_args.unit_group.lower(), data)
        unit_data = ConversionData(unit_group=parsed_args.unit_group.lower())
        if unit_data.unit_group == "time":
            unit_data.time_input = " ".join(arg.lower() for arg in parsed_args.args)
            unit_data.validate_for_conversion(data)
            converter_time(data, unit_data)
        else:
            if len(parsed_args.args) not in [2, 3]:
                raise ValueError("Invalid format for non-time conversion! Usage: <from_type> <to_type> [amount]")
            unit_data.from_type = resolve_aliases(data, unit_data.unit_group, parsed_args.args[0].lower())
            unit_data.to_type = resolve_aliases(data, unit_data.unit_group, parsed_args.args[1].lower())
            unit_data.amount = float(parsed_args.args[2]) if len(parsed_args.args) == 3 else 1.0
            unit_data.validate_for_conversion(data)
            unit_data.new_value = converter(data, unit_data)
            print(f"{format_value(unit_data.amount)} {unit_data.from_type} = {format_value(unit_data.new_value)} {unit_data.to_type}")

    elif parsed_args.command in ["manage-group", "mg"]:
        unit_data = ManageGroupData(
            unit_group = parsed_args.unit_group.lower(),
            action = parsed_args.action.lower(),
        )
        if parsed_args.new_base_unit is not None:
            unit_data.new_base_unit = parsed_args.new_base_unit.lower()
        unit_data.validate_action()
        if unit_data.action == "add":
            unit_data.validate_add_action(data)            
        elif unit_data.action == "remove":
            validate_unit_group(unit_data.unit_group, data)
            unit_data.validate_remove_action(data)            
        manage_group(data, unit_data)

    elif parsed_args.command in ["manage-type", "mt"]:
        validate_unit_group(parsed_args.unit_group.lower(), data)
        unit_data = ManageTypeData(
            unit_group = parsed_args.unit_group.lower(),
            unit_type = parsed_args.unit_type.lower(),
            action = parsed_args.action.lower(),
            value = parsed_args.value,
            factor = parsed_args.factor,
            offset = parsed_args.offset
        )
        unit_data.validate_for_manage_type(data)
        # Adds temperature type
        if unit_data.action == "add" and unit_data.unit_group == "temperature":
            add_temp_type(data, unit_data)
        else:
            manage_type(data, unit_data)

    elif parsed_args.command in ["aliases", "a"]:
        validate_unit_group(parsed_args.unit_group.lower(), data)
        unit_data = AliasesData(
            unit_group = parsed_args.unit_group.lower(),
            unit_type = parsed_args.unit_type.lower(),
            action = parsed_args.action.lower(),
            alias = parsed_args.alias.lower()
        )
        unit_data.validate_for_aliases(data)
        manage_aliases(data, unit_data)

    elif parsed_args.command in ["change-base", "cb"]:
        validate_unit_group(parsed_args.unit_group.lower(), data)
        unit_data = ChangeBaseData(
            unit_group=parsed_args.unit_group.lower(),
            new_base_unit = resolve_aliases(data, parsed_args.unit_group.lower(), parsed_args.new_base_unit.lower())
        )
        unit_data.validate_for_change_base(data)
        change_base_unit(data, unit_data)


def get_action(data) -> None:
    while True:
        try:
            action: str = get_users_input("Let's begin! What do you want to do? ").strip().lower()
            # Adds logic to check action validity
            if action in ["groups", "g"]:
                print_groups(data)
                continue
            elif action in ["history", "h"]:
                print_history(data)
                continue
            elif action in ["types", "t"]:                
                print_types(data)
                continue
            elif action in ["convert", "c"]:
                conversion_logic(data)
                continue
            elif action in ["manage-type", "mt"]:
                manage_type(data)
                continue
            elif action in ["manage-group", "mg"]:
                manage_group(data)
                continue
            elif action in ["aliases", "a"]:
                manage_aliases(data)
                continue
            elif action in ["change-base", "cb"]:
                change_base_unit(data)
                continue
            else:
                raise ValueError(f"'{action}' is not a valid action!")
        except (EOFError, KeyboardInterrupt):
            sys.exit("Bye!")
        except (KeyError, ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
            continue


def get_unit_group(data) -> str:
    """Gets unit group"""
    unit_group: str = get_users_input("Unit group: ").strip().lower()
    validate_unit_group(unit_group, data)
    return unit_group

def print_groups(data) -> None:
    """Prints all available group of units"""
    print("Groups: " + ", ".join(data.units.keys()))


def print_history(data, limit: int = 10) -> None:
    """Prints previous conversion request (default = last 10 entries)"""
    if not data.conversion_log:
        print("Conversion history is empty!")
        return        
    
    for entry in data.conversion_log[-limit:]:  # Gets the last 10 entries
        if entry["unit_group"] == "time":
            if entry["from_time"] in data.units["time"]:
                print(f"{format_value(entry['factor_time'])} {entry['from_time']} = {format_value(entry['result'])} {entry['to_time']} (Group: {entry['unit_group']})")
            elif ":" in entry["from_time"] or entry["from_time"] in data.all_months or "-" in entry["from_time"]:
                print(f"{format_value(entry['result'])} {entry['factor_time']} between {entry['from_time']} {entry['to_time']} (Group: {entry['unit_group']})")
            elif len(entry["from_time"].split()) > 1:
                print(f"{entry["from_time"]} = {format_value(entry["result"])} {entry["to_time"]}")
        else:
            print(f"{format_value(entry['amount'])} {entry['from_type']} = {format_value(entry['result'])} {entry['to_type']} (Group: {entry['unit_group']})")


def print_types(data, unit_group=None) -> None:
    """Prints all unit types for a specific unit group"""
    if unit_group is None:
        unit_group = get_unit_group(data)
    # Used to construct the sequence of unit_type with its respective aliases
    formatted_output = []
    # Iterates over the outter keys of 'units' dictionary
    for unit_type in data.units[unit_group]:
        # Gets all aliases for a specific unit type
        aliases = [alias for alias, unit in data.unit_aliases.get(unit_group, {}).items() if unit == unit_type]
        if aliases:
            formatted_output.append(f"{unit_type} ({', '.join(f'\'{alias}\'' for alias in aliases)})")
        else:
            formatted_output.append(unit_type)

    print(f"'{unit_group}' units: " + ", ".join(formatted_output))


def conversion_logic(data) -> None:
    """Handles all logic of unit conversion"""
    unit_group: str = get_unit_group(data)
    unit_data = ConversionData(unit_group)
    if unit_data.unit_group == "time":
        print_time_instructions()
        unit_data.time_input = get_users_input("Enter time conversion: ").strip().lower()
        unit_data.validate_time_input()
        converter_time(data, unit_data)
        return
    unit_data.from_type, unit_data.to_type = get_converter_units(data, unit_data)
    unit_data.amount = get_amount(unit_data)
    unit_data.validate_for_conversion(data)
    unit_data.new_value = converter(data, unit_data)

    print(f"{format_value(unit_data.amount)} {unit_data.from_type} = {format_value(unit_data.new_value)} {unit_data.to_type}")   


def converter(data, unit_data) -> float:
    """Convert one value to another"""
    unit_data.validate_for_conversion(data)
    # Separates conversion logic when dealing with temperature
    if unit_data.unit_group == "temperature":
        unit_data.new_value = converter_temp(data, unit_data)
        # Adds to log file
    else:
        zero_division_checker(float(data.units[unit_data.unit_group][unit_data.to_type]))
        unit_data.new_value = unit_data.amount * (data.units[unit_data.unit_group][unit_data.from_type]/data.units[unit_data.unit_group][unit_data.to_type])

    # Adds to log file
    add_to_log(data, unit_data)
    return unit_data.new_value


def converter_temp(data, unit_data) -> float:
    """Handles conversion for temperature units"""
    # Get's conversion factor and offset for temperature calculation
    factor_from, offset_from = data.units[unit_data.unit_group][unit_data.from_type]
    factor_to, offset_to = data.units[unit_data.unit_group][unit_data.to_type]
    if unit_data.from_type == "celsius":
        return (unit_data.amount * factor_to) + offset_to
    zero_division_checker(factor_from)
    temp_in_celsius = (unit_data.amount - offset_from) / factor_from
    if unit_data.to_type == "celsius":
        return temp_in_celsius
    return (temp_in_celsius * factor_to) + offset_to


def converter_time(data, unit_data) -> None:
    """Handles conversion for time units"""
    unit_data.validate_time_args(data)
    args = unit_data.time_input.split()
    if len(args) == 2:
        converter_time_2args(data, unit_data)    
    elif len(args) == 3:
        converter_time_3args(data, unit_data)
    # E.g. 5 years 10 months 10 days 8 hours 56 minutes seconds
    elif len(args) % 2 != 0 and len(args) > 3:
        unit_data.to_time = args[-1]
        zero_division_checker(data.units[unit_data.unit_group][unit_data.to_time])
        formatted_value = []
        total_seconds = 0
        for number, unit in zip(args[0::2], args[1::2]):
            number = float(number)
            unit = resolve_aliases(data, unit_data.unit_group, unit)
            total_seconds += number * data.units[unit_data.unit_group][unit]
            formatted_value.append((format_value(number), unit))

        unit_data.from_time = " ".join(f"{num} {unit}" for num, unit in formatted_value)
        unit_data.new_time = total_seconds / data.units[unit_data.unit_group][unit_data.to_time]

        print(f"{' '.join(f'{num} {unit}' for num, unit in formatted_value)} = {format_value(unit_data.new_time)} {unit_data.to_time}")
        add_to_log(data, unit_data, is_time_convertion=True)


def converter_time_3args(data, unit_data):
    unit_group = unit_data.unit_group
    from_time = unit_data.from_time
    to_time = unit_data.to_time
    factor_time = unit_data.factor_time

    # E.g. minutes seconds 1
    if from_time in data.units[unit_group] and to_time in data.units[unit_group]:           
        total_seconds = factor_time * data.units[unit_group][from_time]
        zero_division_checker(data.units[unit_group][to_time])
        unit_data.new_time = total_seconds / data.units[unit_group][to_time]
        print(f"{format_value(factor_time)} {from_time} = {format_value(unit_data.new_time)} {to_time}")

    else:
        unit_data.validate_factor_time(data)
        zero_division_checker(data.units[unit_group][factor_time])
        
        # E.g. 17h:28m:36s 04h:15m:22s seconds
        if parse_time_input(from_time) is not None and parse_time_input(to_time) is not None:
            new_from_time = parse_time_input(from_time)
            new_to_time = parse_time_input(to_time)
            unit_data.new_time = fabs((new_from_time - new_to_time) / data.units[unit_group][factor_time])
            print(f"There are {format_value(unit_data.new_time)} {factor_time} between {from_time} and {to_time}")
        
        # E.g. JAN DEC days
        elif from_time in data.all_months and to_time in data.all_months:
            from_datetime = datetime(2023, get_index_from_month(data, from_time), 1)
            if get_index_from_month(data, to_time) > get_index_from_month(data, from_time):
                to_datetime = datetime(2023, get_index_from_month(data, to_time), get_days_from_month(data, to_time))
            elif get_index_from_month(data, to_time) < get_index_from_month(data, from_time):
                to_datetime = datetime(2024, get_index_from_month(data, to_time), get_days_from_month(data, to_time))
            else:
                to_datetime = datetime(2023, get_index_from_month(data, to_time), get_days_from_month(data, to_time))
            days = abs((from_datetime - to_datetime)).days + 1
            if factor_time == "days":
                unit_data.new_time = days
            else:
                total_seconds = (timedelta(seconds=days * data.units[unit_group]["days"])).total_seconds()
                zero_division_checker(data.units[unit_group][factor_time])
                unit_data.new_time = total_seconds / data.units[unit_group][factor_time]
            print(f"Between {from_time} and {to_time} there are {format_value(unit_data.new_time)} {factor_time}")
        
        # E.g. 2019-11-04 2056-04-28 days
        elif parse_date_input(from_time) is not None and parse_date_input(to_time) is not None:
            year_duration = 365
            try:
                from_years, from_months, from_days = parse_date_input(from_time)
                validate_date(from_years, from_months, from_days)
                to_years, to_months, to_days = parse_date_input(to_time)
                validate_date(to_years, to_months, to_days)
            except ValueError:
                raise ValueError("Invalid date!")
            from_total_days = from_years * year_duration
            to_total_days = to_years * year_duration
            for month in range(1, from_months):
                from_total_days += gets_days_from_index(data, str(month))
            for month in range(1, to_months):
                to_total_days += gets_days_from_index(data, str(month))
            from_total_days += from_days
            to_total_days += to_days
            
            leap_years = calculate_leap_years(from_years, from_months, to_years, to_months, to_days)
            total_days = abs((from_total_days - to_total_days)) + 1 + leap_years
            total_seconds = total_days * data.units[unit_group]["days"]
            unit_data.new_time = total_seconds / data.units[unit_group][factor_time]        
            print(f"Between {from_time} and {to_time} there are {format_value(unit_data.new_time)} {factor_time}")

        # Any other format is invalid!
        else:
            print("Invalid time conversion format!")
            return

    unit_data.unit_group = unit_group
    unit_data.from_time=from_time
    unit_data.to_time=to_time
    unit_data.factor_time=factor_time
    add_to_log(data, unit_data, is_time_convertion=True)


def converter_time_2args(data, unit_data):
    unit_group = unit_data.unit_group
    from_time = unit_data.from_time
    factor_time = unit_data.factor_time   
    zero_division_checker(data.units[unit_group][factor_time])

    # E.g. 17h:28m:36s seconds
    if parse_time_input(from_time) is not None:
        total_seconds = parse_time_input(from_time)
        unit_data.new_time = (total_seconds / data.units[unit_group][factor_time])
        print(f"There are {format_value(unit_data.new_time)} {factor_time} in {from_time}")

    # E.g. JAN minutes
    elif from_time in data.all_months:
        days = get_days_from_month(data, from_time)
        total_seconds = days * data.units[unit_group]["days"]
        unit_data.new_time = total_seconds / data.units[unit_group][factor_time]
        print(f"There are {format_value(unit_data.new_time)} {factor_time} in {from_time}")

    # E.g. 2019-11-04 days
    elif parse_date_input(from_time) is not None:
        years, months, days = parse_date_input(from_time)
        total_seconds = get_seconds(data, unit_group, years, months, days)
        unit_data.new_time = total_seconds / data.units[unit_group][factor_time]
        print(f"There are {format_value(unit_data.new_time)} {factor_time} in {years} years, {months} months, {days} days")

    unit_data.unit_group = unit_group
    unit_data.from_time=from_time
    unit_data.factor_time=factor_time
    add_to_log(data, unit_data, is_time_convertion=True)


def manage_group(data, unit_data=None) -> None:
    """Handles all logic of adding and removing unit groups"""    
    if unit_data is None:
        unit_data = ManageGroupData(unit_group = None)
    if unit_data.action is None:
        unit_data.action = get_users_input(f"Existed groups: {", ".join(data.units.keys())}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()
    unit_data.validate_action()
    if unit_data.action == "add":
        if unit_data.unit_group is None:
            unit_data.unit_group = get_users_input(f"Unit group: ").strip().lower()
        unit_group = unit_data.unit_group
        if unit_group in data.units:
            raise ValueError(f"'{unit_group}' is already an existed group!")
        if unit_data.new_base_unit is None:
            unit_data.new_base_unit = get_users_input(f"You are creating '{unit_group}' group. Enter the base unit for that group: ").strip().lower()
        new_base_unit = unit_data.new_base_unit
        if not new_base_unit:
            raise ValueError("You need to specify the base unit to create a new group")
        print(f"You've just created a '{unit_group}' group, with '{new_base_unit}' as its base unit!")
        data.units[unit_group] = {}
        data.units[unit_group][new_base_unit] = 1.0
        data.base_units[unit_group] = new_base_unit
        data.unit_aliases[unit_group] = {}
    elif unit_data.action == "remove":
        if unit_data.unit_group is None:
            unit_data.unit_group = get_unit_group(data)
        data.units.pop(unit_data.unit_group)
        data.base_units.pop(unit_data.unit_group)
        data.unit_aliases.pop(unit_data.unit_group)
        print(f"Group '{unit_data.unit_group}' successfullu removed!")
    save_data(data.units, "units")
    save_data(data.base_units, "base_units")
    save_data(data.unit_aliases, "unit_aliases")
    
    
def manage_type(data, unit_data=None) -> None:
    """Handles all logic of adding and removing unit types"""
    if unit_data is None:
        unit_data = ManageTypeData(unit_group = get_unit_group(data))
    if unit_data.action is None:
        unit_data.action = get_users_input(f"Existed types for '{unit_data.unit_group}' group: {data.units[unit_data.unit_group]}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()
    unit_data.validate_action()
    if unit_data.action == "add":
        if unit_data.unit_type is None:
            unit_data.unit_type = get_users_input(f"Enter new type for '{unit_data.unit_group}' group: ").strip().lower()
        unit_data.validate_add_action(data)
        if unit_data.unit_group == "temperature":
            add_temp_type(data, unit_data)
            return
        if unit_data.value is None:
            unit_data.value = get_users_input(f"Enter conversion factor to base unit '{data.base_units[unit_data.unit_group]}' of '{unit_data.unit_group}' group: ").strip().lower()
        unit_data.validate_value()
        data.units[unit_data.unit_group][unit_data.unit_type] = unit_data.value
        print(f"A new unit type was added on '{unit_data.unit_group}' group: {unit_data.unit_type} = {unit_data.value}")
    elif unit_data.action == "remove":
        if unit_data.unit_type is None:
            unit_data.unit_type = get_users_input(f"Enter type to remove from '{unit_data.unit_group}' group: ").strip().lower()
        unit_data.validate_remove_action(data)
        data.units[unit_data.unit_group].pop(unit_data.unit_type)
        aliases_to_remove = [alias for alias, unit in data.unit_aliases[unit_data.unit_group].items() if unit == unit_data.unit_type]
        for alias in aliases_to_remove:
            data.unit_aliases[unit_data.unit_group].pop(alias)
        print(f"'{unit_data.unit_type}' was removed from '{unit_data.unit_group}'")
    save_data(data.units, "units")
    save_data(data.unit_aliases, "unit_aliases")


def add_temp_type(data, unit_data) -> None:
    """Handles all logic for adding temperature units"""
    if unit_data.factor == None:
        unit_data.factor = get_users_input(f"Enter conversion factor to base unit '{data.base_units[unit_data.unit_group]}' of 'temperature' group: ").strip().lower()
    unit_data.validate_factor()
    if unit_data.offset == None:
        unit_data.offset = get_users_input(f"Enter offset value to base unit '{data.base_units[unit_data.unit_group]}' of 'temperature' group: ").strip().lower()
    unit_data.validate_offset()
    data.units[unit_data.unit_group][unit_data.unit_type] = [unit_data.factor, unit_data.offset]
    print(f"A new unit type was added on temperature group: {unit_data.unit_type} = [{unit_data.factor}, {unit_data.offset}]")
    save_data(data.units, "units")


def manage_aliases(data, unit_data=None):
    """Handles aliases, allowing users to add or remove aliases to/from an unit type"""
    if unit_data is None:
        unit_data = AliasesData(unit_group = get_unit_group(data))
    unit_group = unit_data.unit_group
    if unit_data.unit_type is None:
        unit_data.unit_type = resolve_aliases(data, unit_group, get_users_input(f"Enter unit type for '{unit_group}' group: ").strip().lower())
    unit_type = unit_data.unit_type
    all_aliases = [alias for alias in data.unit_aliases[unit_group] if unit_type == data.unit_aliases[unit_group].get(alias)]
    if unit_data.action is None:
        unit_data.action = get_users_input(f"Existed aliases for '{unit_type}': {all_aliases}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()
    action = unit_data.action
    if unit_data.alias is None:
        unit_data.alias = get_users_input(f"Which alias do you want to {action} {"to" if action == "add" else "from"} '{unit_type}'? ").strip().lower()
    alias = unit_data.alias
    unit_data.validate_for_aliases(data)
    if action == "add":
        data.unit_aliases[unit_group][alias] = unit_type
        print(f"Alias successfully added! New alias for '{unit_type}': '{alias}'")
    elif action == "remove":
        data.unit_aliases[unit_group].pop(alias) 
        print(f"'{alias}' successfully removed from '{unit_type}'!")

    save_data(data.unit_aliases, "unit_aliases")


def change_base_unit(data, unit_data=None):
    """Allows change of base unit for a specific unit group"""
    if unit_data is None:
        unit_data = ChangeBaseData(unit_group = get_unit_group(data))
    unit_group = unit_data.unit_group
    if unit_data.new_base_unit is None:
        print(f"All unit types for '{unit_group}' group: " + ", ".join(data.units[unit_group].keys()))
        unit_data.new_base_unit = resolve_aliases(data, unit_group, get_users_input(f"Enter new base unit for '{unit_group}' group: ").strip().lower())
    unit_data.validate_for_change_base(data)

    refactor_value(data, unit_group, unit_data.new_base_unit)
    data.base_units[unit_group] = unit_data.new_base_unit

    save_data(data.units, "units")
    save_data(data.base_units, "base_units")

    print(f"You've just changed the base unit from '{unit_group}' group, to '{unit_data.new_base_unit}'!")


if __name__ == "__main__":
    main()