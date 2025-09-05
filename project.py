import argparse
import calendar
import json
import re
import sys

from datetime import datetime, timedelta
from math import fabs


# Imports dictionaries
try:
    # Opens dictionary with all units available
    with open("units.json", "r") as file:
        units = json.load(file)
    # Opens dictionary of base units for each group
    with open("base_units.json", "r") as file:
        base_units = json.load(file)
    # Opens dictionary containing all conversions history
    with open("conversion_log.json", "r") as file:
        conversion_log = json.load(file)
    # Opens dictionary that relates each month with an index
    with open("month_indexes.json", "r") as file:
        month_indexes = json.load(file)
    # Opens dictionary that contains all aliases for each unit type
    with open("unit_aliases.json", "r") as file:
        unit_aliases = json.load(file)
    with open("month_days.json", "r") as file:
        month_days = json.load(file)
    with open("month_index_days.json", "r") as file:
        month_index_days = json.load(file)
except FileNotFoundError:
    sys.exit("Error: file not found!")
except json.JSONDecodeError:
    sys.exit("Error: file if corrupted!")


def validate_dictionaries(units, base_units, conversion_log, month_indexes, unit_aliases, month_days, month_index_days):
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
    # Ensures 'convert_history' is a list
    if not isinstance(conversion_log, list):
        raise ValueError("'convert_history' structure is corrupted!")
    # Ensures 'month_indexes' is a dictionary and it's not empty
    if not isinstance(month_indexes, dict) or not month_indexes:
        raise ValueError("'month_indexes' structure is corrupted!")
    if not isinstance(month_days, dict) or not month_days:
        raise ValueError("'month_days' structure is corrupted!")
    if not isinstance(month_index_days, dict) or not month_index_days:
        raise ValueError("'month_index_days' structure is corrupted!")
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


validate_dictionaries(units, base_units, conversion_log, month_indexes, unit_aliases, month_days, month_index_days)


def main() -> None:
    # Handles command-line arguments
    try:
        if len(sys.argv) > 1:
            handle_cli(sys.argv)
            sys.exit(0)  # Exits program after command-line execution
    except (ValueError, KeyError, ZeroDivisionError, TypeError) as e:
        print(f"Error: {e}")
        sys.exit(1) # Exits the program if any error happens
    print_introductory_messages()
    get_action()


def handle_cli(args):
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
    convert_parser.add_argument("from_type", help="Source unit type")
    convert_parser.add_argument("to_type", help="Target unit type")
    convert_parser.add_argument("amount", nargs="?", help="Amount to convert")
    # 'add' command
    add_parser = subparser.add_parser("add", aliases=["a"], help="Add new unit group/type")
    add_parser.add_argument("unit_group", help="Unit group")
    add_parser.add_argument("unit_type", help="Unit type to be added")
    add_parser.add_argument("action", choices=["add", "remove"], help="Action to perform")
    add_parser.add_argument("value", nargs="?", help="Conversion factor to base unit (not used for temperature)")
    add_parser.add_argument("--factor", type=float, help="Conversion factor to temperature's base unit")
    add_parser.add_argument("--offset", type=float, help="Offset to temperature")
    # 'aliases' command
    aliases_parser = subparser.add_parser("aliases", aliases=["al"], help="Manage unit's aliases")
    aliases_parser.add_argument("unit_group", help="Unit group")
    aliases_parser.add_argument("unit_type", help="Unit type")
    aliases_parser.add_argument("action", choices=["add", "remove"], help="Action to perform")
    aliases_parser.add_argument("alias", help="Alias used to add/remove to/from an unit")
    # 'change-base' command
    change_base_parser = subparser.add_parser("change-base", aliases=["cb"], help="Change unit base for a group")
    change_base_parser.add_argument("unit_group", help="Unit group")
    change_base_parser.add_argument("new_base_unit", help="New base unit")

    # Parses arguments
    parsed_args = parser.parse_args(formatted_args[1:])  # Skips first argument (program's name)
    # Lowercases arguments
    if parsed_args.command in ["types", "t"]:
        unit_group = parsed_args.unit_group.lower()
    elif parsed_args.command in ["convert", "c"]:
        unit_group = parsed_args.unit_group.lower()
        from_type = parsed_args.from_type.lower()
        to_type = parsed_args.to_type.lower()
    elif parsed_args.command in ["add", "a"]:
        unit_group = parsed_args.unit_group.lower()
        unit_type = parsed_args.unit_type.lower()
        action = parsed_args.action.lower()
    elif parsed_args.command in ["aliases", "al"]:
        unit_group = parsed_args.unit_group.lower()
        unit_type = parsed_args.unit_type.lower()
        action = parsed_args.action.lower()
        alias = parsed_args.alias.lower()
    elif parsed_args.command in ["change-base", "cb"]:
        unit_group = parsed_args.unit_group.lower()
        new_base_unit = parsed_args.new_base_unit.lower()
    
    # Calls argument respective function
    if parsed_args.command in ["groups", "g"]:
        print_groups()
    elif parsed_args.command in ["history", "h"]:
        print_history(parsed_args.limit)
    elif parsed_args.command in ["types", "t"]:
        print_types(unit_group)
    elif parsed_args.command in ["convert", "c"]:
        if unit_group == "time":
            converter_time(unit_group, from_type, to_type, parsed_args.amount)
        else:
            from_type = resolve_aliases(unit_group, from_type)
            to_type = resolve_aliases(unit_group, to_type)
            if not parsed_args.amount:
                raise ValueError("You need to enter an amount to convert!")
            try:
                amount = float(parsed_args.amount)
            except (ValueError, TypeError):
                raise ValueError(f"'{parsed_args.amount}' is an invalid amount!")
            new_value = converter(amount, unit_group, from_type, to_type)
            print(f"{format_value(amount)} {from_type} = {format_value(new_value)} {to_type}")
    elif parsed_args.command in ["add", "a"]:
        # Adds temperature type
        if unit_group == "temperature":
            if parsed_args.factor is None or parsed_args.offset is None:
                raise ValueError("Adding temperature type requires --factor and --offset")
            add_temp_type(unit_group, unit_type, action, parsed_args.factor, parsed_args.offset)
        # Adds unit type for existed group
        elif unit_group in units:
            if parsed_args.value is None:
                raise ValueError("Adding non-temperature type requires a value")
            manage_type(unit_group, unit_type, parsed_args.value, action)
        # Creates new group and new type
        else:
            add_new_group(unit_group)
    elif parsed_args.command in ["aliases", "al"]:
        manage_aliases(unit_group, unit_type, action, alias)
    elif parsed_args.command in ["change-base", "cb"]:
        change_base_unit(unit_group, new_base_unit)


def resolve_aliases(unit_group, unit_type):
    """Checks user's input for any match with unit type or unit's aliases"""
    # Checks for literal name
    if unit_type in units[unit_group]:
        return unit_type
    # Checks for aliases
    elif unit_type in unit_aliases[unit_group]:
        return unit_aliases[unit_group][unit_type]
    else:
        return False


def print_introductory_messages() -> None:
    """Prints introductory messages and instructions"""
    print("Welcome to unit converter!")
    print("To check all group of units available, enter 'groups'")
    print("To check all types for a specific group, enter 'types'")
    print("To convert an unit, enter 'convert'")
    print("To add a new unit group or a new unit type, enter 'add'")
    print("Quit anytime by entering 'quit' or by pressing ctrl+d or ctrl+c", end="\n\n")


def get_action() -> None:
    while True:
        try:
            action: str = input("Let's begin! What do you want to do? ").strip().lower()
            # Adds logic to check action validity
            if action in ["groups", "g"]:
                print_groups()
                continue
            elif action in ["history", "h"]:
                print_history()
                continue
            elif action in ["types", "t"]:                
                print_types()
                continue
            elif action in ["convert", "c"]:
                conversion_logic()
                continue
            elif action in ["add", "a"]:
                manage_type()
                continue
            elif action in ["aliases", "al"]:
                manage_aliases()
                continue
            elif action in ["change-base", "cb"]:
                change_base_unit()
                continue
            elif action == "quit":
                sys.exit("Bye!")
            else:
                raise ValueError(f"'{action}' is not a valid action!")
        except (EOFError, KeyboardInterrupt):
            sys.exit("Bye!")
        except (KeyError, ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
            continue


def print_groups() -> None:
    """Prints all available group of units"""
    print("Groups: " + ", ".join(units.keys()))


def print_history(limit: int = 10) -> None:
    """Prints previous conversion request (default = last 10 entries)"""
    if not conversion_log:
        print("Conversion history is empty!")
        return
    for entry in conversion_log[-limit:]:  # Gets the last 10 entries
        if entry["unit_group"] == "time":
            if entry["from_time"] in units["time"]:
                print(f"{format_value(entry['factor_time'])} {entry['from_time']} = {format_value(entry['result'])} {entry['to_time']} (Group: {entry['unit_group']})")
            elif ":" in entry["from_time"] or entry["from_time"] in month_indexes or "-" in entry["from_time"]:
                print(f"{format_value(entry['result'])} {entry['factor_time']} between {entry['from_time']} {entry['to_time']} (Group: {entry['unit_group']})")
        else:
            print(f"{format_value(entry['amount'])} {entry['from_type']} = {format_value(entry['result'])} {entry['to_type']} (Group: {entry['unit_group']})")


def print_types(unit_group=None) -> None:
    """Prints all unit types for a specific unit group"""
    if unit_group is None:
        unit_group: str = get_unit_group()
    # Used to construct the sequence of unit_type with its respective aliases
    formated_output = []
    # Iterates over the outter keys of 'units' dictionary
    for unit_type in units[unit_group]:
        # Gets all aliases for a specific unit type
        aliases = [alias for alias, unit in unit_aliases.get(unit_group, {}).items() if unit == unit_type]
        if aliases:
            formated_output.append(f"{unit_type} ({', '.join(f'\'{alias}\'' for alias in aliases)})")
        else:
            formated_output.append(unit_type)

    print("Units: " + ", ".join(formated_output))


def conversion_logic() -> None:
    """Handles all logic of unit conversion"""
    unit_group: str = get_unit_group()
    if unit_group == "time":
        converter_time(unit_group)
        return
    from_type, to_type = get_converter_units(unit_group)
    amount: float = get_amount(from_type)
    new_value: str = converter(amount, unit_group, from_type, to_type)

    print(f"{format_value(amount)} {from_type} = {format_value(new_value)} {to_type}")   


def get_unit_group() -> str:
    """Gets unit group"""
    unit_group: str = input("Unit group: ").strip().lower()
    if not unit_group:
        raise ValueError("Unit group cannot be empty!")
    if unit_group not in units:
        raise KeyError(f"{unit_group} is not a valid group!")
    return unit_group


def get_converter_units(unit_group) -> tuple[str, str]:
    """Gets types of units"""
    from_type: str = resolve_aliases(unit_group, input("From: ").strip().lower())
    to_type: str = resolve_aliases(unit_group, input("To: ").strip().lower())
    if not from_type or not to_type:
        raise ValueError("Unit type cannot be empty!")
    if from_type not in units[unit_group] or to_type not in units[unit_group]:
        raise KeyError("Invalid unit type!")
    return from_type, to_type


def get_amount(from_type) -> float:
    """Gets unit amount"""
    amount: str = input("Amount: ").strip()
    if not amount:
        raise ValueError("Amount cannot be empty")        
    # Ensures amount is a number
    elif not re.search(r"^-?\d+(\.\d+)?$", amount):
        raise ValueError("Invalid amount! Please, insert integer or decimals! (e.g. 10 or 10.0)")        
    try:
        amount = float(amount)
    except:
        raise ValueError("Invalid amount!")   
    # Prevents negative value for "Kelvin"  
    if amount < 0 and from_type == "kelvin":
        raise ValueError("Kelvin temperature cannot be negative!")
    return float(amount)


def converter(amount, unit_group, from_type, to_type) -> float:
    """Convert one value to another"""
    # Separates conversion logic when dealing with temperature
    if unit_group == "temperature":
        new_temp = converter_temp(amount, unit_group, from_type, to_type)
        # Adds to log file
        add_to_log(unit_group=unit_group, from_type=from_type, to_type=to_type, amount=amount, new_value=new_temp)
        return new_temp   
    
    if float(units[unit_group][to_type]) == 0:
        raise ZeroDivisionError("Can't divide by zero!")
    new_value = amount * (units[unit_group][from_type]/units[unit_group][to_type])
    # Adds to log file
    add_to_log(unit_group=unit_group, from_type=from_type, to_type=to_type, amount=amount, new_value=new_value)

    return new_value


def converter_temp(amount, unit_group, from_type, to_type) -> float:
    """Handles conversion for temperature units"""
    # Get's conversion factor and offset for temperature calculation
    factor_from, offset_from = units[unit_group][from_type]
    factor_to, offset_to = units[unit_group][to_type]
    if from_type == "celsius":
        return (amount * factor_to) + offset_to
    if factor_from == 0:
        raise ZeroDivisionError("Can't divide by zero!")
    temp_in_celsius = (amount - offset_from) / factor_from
    if to_type == "celsius":
        return temp_in_celsius
    return (temp_in_celsius * factor_to) + offset_to


def converter_time(unit_group, from_time=None, to_time=None, factor_time=None) -> None:
    """Handles conversion for time units"""
    if from_time is None or to_time is None or factor_time is None:
        print_time_instructions()
        time_input = input("Enter time conversion: ").strip().lower()
        if not time_input:
            raise ValueError("Time conversion can't be empty! Enter an expression!")

    if len(time_input.split()) == 2:
        try:
            from_time, factor_time = time_input.split(" ")
        except ValueError:
            raise ValueError("Invalid format for date and time conversion!")
        converter_time_2args(unit_group, from_time, factor_time)
        return
    elif len(time_input.split()) == 3:
        try:
            from_time, to_time, factor_time = time_input.split(" ")
        except ValueError:
            raise ValueError("Invalid format for date and time conversion!")
        converter_time_3args(unit_group, from_time, to_time, factor_time)
        return

    elif len(time_input.split()) % 2 == 0 and len(time_input.split()) > 2:
        ...
        
    else:
        raise ValueError("Invalid format for date and time conversion!")


def converter_time_3args(unit_group, from_time, to_time, factor_time):
    # E.g. seconds minutes 10
    if resolve_aliases(unit_group, from_time) in units[unit_group] and resolve_aliases(unit_group, to_time) in units[unit_group]:
        from_time = resolve_aliases(unit_group, from_time)
        to_time = resolve_aliases(unit_group, to_time)
        try:
            factor_time = float(factor_time)
        except ValueError:
            raise ValueError("Enter a valid value for conversion!")            
        total_seconds = factor_time * units[unit_group][from_time]
        if units[unit_group][to_time] == 0:
            raise ZeroDivisionError("Can't divide by zero!")
        new_time = total_seconds / units[unit_group][to_time]
        print(f"{format_value(factor_time)} {from_time} = {format_value(new_time)} {to_time}")

    else:
        factor_time = resolve_aliases(unit_group, factor_time)
        if factor_time not in units[unit_group]:
            raise KeyError(f"Unit type '{factor_time}' not found in '{unit_group}' group!")
        if units[unit_group][factor_time] == 0:
            raise ZeroDivisionError("Can't divide by zero!")
        
        # E.g. 17h:28m:36s 04h:15m:22s seconds
        if parse_time_input(from_time) is not None and parse_time_input(to_time) is not None:
            new_from_time = parse_time_input(from_time)
            new_to_time = parse_time_input(to_time)
            new_time = fabs((new_from_time - new_to_time) / units[unit_group][factor_time])
            print(f"There are {format_value(new_time)} {factor_time} between {from_time} and {to_time}")
        
        # E.g. JAN NOV minutes
        elif from_time in month_indexes and to_time in month_indexes:
            from_datetime = datetime(2023, month_indexes[from_time], 1)
            if month_indexes[to_time] > month_indexes[from_time]:
                to_datetime = datetime(2023, month_indexes[to_time], month_days[to_time])
            elif month_indexes[to_time] < month_indexes[from_time]:
                to_datetime = datetime(2024, month_indexes[to_time], month_days[to_time])
            else:
                to_datetime = datetime(2023, month_indexes[to_time], month_days[to_time])
            days = abs((from_datetime - to_datetime)).days + 1
            if factor_time == "days":
                new_time = days
            else:
                total_seconds = (timedelta(seconds=days * units[unit_group]["days"])).total_seconds()
                if units[unit_group][factor_time] == 0:
                    raise ZeroDivisionError("Can't divide by zero!")
                new_time = total_seconds / units[unit_group][factor_time]
            print(f"Between {from_time} and {to_time} there are {format_value(new_time)} {factor_time}")
        
        # E.g. 2019-11-04 2056-04-28 days
        elif parse_date_input(from_time) is not None and parse_date_input(to_time) is not None:
            year_duration = 365
            try:
                from_years, from_months, from_days = parse_date_input(from_time)
                validate_date(from_years, from_months, from_days)
                to_years, to_months, to_days = parse_date_input(to_time)
                validate_date(to_years, to_months, to_days)
            except ValueError:
                return
            leap_years = calculate_leap_years(from_years, from_months, from_days, to_years, to_months, to_days)
            if is_leap(from_years):
                if from_months >= 2:
                    month_index_days["2"] = 29
            from_total_days = from_years * year_duration + sum(month_index_days[str(i)] for i in range(from_months, 13)) - from_days
            month_index_days["2"] = 28
            if is_leap(to_years):
                if to_months >= 2:
                    month_index_days["2"] = 29                
            to_total_days = to_years * year_duration + sum(month_index_days[str(i)] for i in range(1, to_months)) + to_days
            total_days = abs((from_total_days - to_total_days)) + 1 + leap_years
            total_seconds = total_days * units[unit_group]["days"]
            new_time = total_seconds / units[unit_group][factor_time]        
            print(f"Between {from_time} and {to_time} there are {format_value(new_time)} {factor_time}")

        # Any other format is invalid!
        else:
            print("Invalid time conversion format!")
            return

    add_to_log(unit_group=unit_group, from_time=from_time, to_time=to_time, factor_time=factor_time, new_time=new_time, is_time_convertion=True)


def converter_time_2args(unit_group, from_time, factor_time):
    factor_time = resolve_aliases(unit_group, factor_time)
    if factor_time not in units[unit_group]:
        raise KeyError(f"Unit type '{factor_time}' not found in '{unit_group}' group!")      
    if units[unit_group][factor_time] == 0:
        raise ZeroDivisionError("Can't divide by zero!")

    # E.g. 17h:28m:36s seconds
    if parse_time_input(from_time) is not None:
        total_seconds = parse_time_input(from_time)
        new_time = (total_seconds / units[unit_group][factor_time])
        print(f"There are {format_value(new_time)} {factor_time} in {from_time}")

    # E.g. JAN minutes
    elif from_time in month_indexes:
        days = month_days[from_time]
        total_seconds = days * units[unit_group]["days"]
        new_time = total_seconds / units[unit_group][factor_time]
        print(f"There are {format_value(new_time)} {factor_time} in {from_time}")

    # E.g. 2019-11-04 days
    elif parse_date_input(from_time) is not None:
        years, months, days = parse_date_input(from_time)
        total_seconds = get_seconds(unit_group, years, months, days)
        new_time = total_seconds / units[unit_group][factor_time]
        print(f"There are {format_value(new_time)} {factor_time} in {years} years, {months} months, {days} days")

    # Any other format is invalid!
    else:
        print("Invalid time conversion format!")
        return

    add_to_log(unit_group=unit_group, from_time=from_time, factor_time=factor_time, new_time=new_time, is_time_convertion=True)


def print_time_instructions():
    """Prints instructions for converting date and time units"""
    print("For date-time conversion, you can choose from different approaches for conversion:")
    print(" - From a specific unit to another. Usage: <unit_type> <unit_type> quantity")
    print(" - From a more complex time to another. Usage: HH:MM:SS HH:MM:SS <unit_type>")
    print(" - From one month to another. Usage: <month_name> <month_name> <unit_type>")
    print(" - From a date to another. Usage: YYYY-MM-DD YYYY-MM-DD <unit_type>")


def parse_time_input(time_str):
    """Gets user's input of a time and outputs that correspondent value in seconds"""
    if matches := re.search(r"^(?:(\d+)h:)?(?:(\d+)m:)?(?:(\d+)s)?$", time_str):
        hours, minutes, seconds = matches.group(1), matches.group(2), matches.group(3)
        hours = check_time_is_none(hours)
        minutes = check_time_is_none(minutes)
        seconds = check_time_is_none(seconds)

        return hours * 3600 + minutes * 60 + seconds
    return None


def check_time_is_none(time_str):
    if time_str is not None:
        return int(time_str)
    else:
        return 0


def get_seconds(unit_group, years, months, days):
    approx_year_duration = 365.2425 * units[unit_group]["days"]
    approx_month_duration = 30.436875 * units[unit_group]["days"]
    return years * approx_year_duration + months * approx_month_duration + days * units[unit_group]["days"]


def parse_date_input(time_str):
    """Gets user's input of a date, and outputs the year, month and day"""
    if matches := re.search(r"^(\d+)-(\d+)-(\d+)$", time_str):
        year, month, day = map(int, matches.groups())
        return year, month, day
    return None


def calculate_leap_years(from_years, from_months, from_days, to_years, to_months, to_days):
    """Calculates the number of leap years from a date range"""
    years_divided_by_4 = (to_years // 4) - ((from_years-1) // 4)
    years_divided_by_100 = (to_years // 100) - ((from_years-1) // 100)
    years_divided_by_400  = (to_years // 400) - ((from_years-1) // 400)
    leap_year_counter = years_divided_by_4 - years_divided_by_100 + years_divided_by_400
    
    if is_leap(from_years):
        if from_months > 2:
            leap_year_counter -= 1
    if is_leap(to_years):
        if to_months < 2 or (to_months == 2 and to_days < 29):
            leap_year_counter -= 1
    return leap_year_counter


def is_leap(time_int):
    if (time_int % 4 == 0 and time_int % 100 != 0) or (time_int % 400 == 0):
        return True
    return False


def validate_date(year, month, day):
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid date! '{month}' is not a valid month")
    max_days = calendar.monthrange(year, month)[1]
    if not 1 <= day <= max_days:
         raise ValueError(f"Invalid date! '{day}' is not a valid day for '{month}'")
    return True


def add_to_log(unit_group, from_type=None, to_type=None, amount=None, new_value=None, from_time=None, to_time=None, factor_time=None, new_time=None, is_time_convertion=False) -> None:
    """Adds successfully converted value to log file (conversion_log.json)"""
    global conversion_log
    if is_time_convertion:
        if None in (from_time, to_time, factor_time, new_time):
            raise ValueError("Missing required argument!")
        entry = {
        "unit_group": unit_group,
        "from_time": from_time,
        "to_time": to_time,
        "factor_time": factor_time,
        "result": float(new_time)
    }
    else:
        if None in (from_type, to_type, amount, new_value):
            raise ValueError("Missing required argument!")            
        entry = {
            "unit_group": unit_group,
            "from_type": from_type,
            "to_type": to_type,
            "amount": amount,
            "result": float(new_value)
        }
    conversion_log.append(entry)
    try:
        conversion_log_backup = conversion_log.copy()
        with open("conversion_log.json", "w") as file:
            json.dump(conversion_log, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to conversion_log.json!")
        conversion_log = conversion_log_backup


def format_value(value: float) -> str:
    """Format converted value by allowing only 5 decimal values and elimitating all trailling zeroes"""
    formatted_value = f"{value:,.5f}".rstrip("0").rstrip(".")
    # Adds '.0' if formatted value ended up with no decimal values
    if "." not in formatted_value:
        formatted_value += ".0"
    return formatted_value


def manage_type(unit_group=None, unit_type=None, value=None, action=None) -> None:
    """Handles all logic of adding new unit type"""
    global units
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if not unit_group:
        raise ValueError("Enter a group name before proceeding!")    
    elif unit_group not in units:
        add_new_group(unit_group)
        return
    if action is None:
        action = input(f"Existed types for '{unit_group}' group: {units[unit_group]}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()    
    if not action or action not in ["add", "remove"]:
        raise ValueError(f"Invalid action. Decide if you want to 'add' or 'remove' an alias for '{unit_type}'")
    elif action == "add":
        if unit_type is None:
            unit_type: str = input(f"Enter new type for '{unit_group}' group: ").strip().lower()
        if not unit_type:
            raise ValueError("You can't leave that field empty!")
        if unit_type in units:
            raise KeyError(f"'{unit_type}' is already an unit group name!")
        elif unit_type in units[unit_group]:
            raise ValueError(f"'{unit_type}' is already an unit type!")
        elif unit_type in unit_aliases[unit_group]: 
            raise ValueError(f"'{unit_type}' is already being used as an alias in '{unit_group}' group")
        if unit_group == "temperature":
            add_temp_type(unit_group, unit_type, action="add")
            return
        if value is None:
            value: str = input(f"Enter conversion factor to base unit '{base_units[unit_group]}' of '{unit_group}' group: ").strip().lower()
        if not value:
            raise ValueError("You can't leave that field empty!")
        try:
            value = float(value)
        except:
            raise ValueError("Invalid value!")
        units[unit_group][unit_type] = value
        print(f"A new unit type was added on '{unit_group}' group: {unit_type} = {value}")
    elif action == "remove":
        if unit_type is None:
            unit_type: str = input(f"Enter new type for '{unit_group}' group: ").strip().lower()
        if not unit_type:
            raise ValueError("You can't leave that field empty!")
        elif unit_type not in units[unit_group]:
            raise ValueError(f"'{unit_type}' is not an unit type in '{unit_group}' group!")
        elif unit_type == base_units[unit_group]:
            raise ValueError("Cannot remove base unit!")
        units[unit_group].pop(unit_type)
        aliases_to_remove = [alias for alias, unit in unit_aliases[unit_group] if unit == unit_type]
        for alias in aliases_to_remove:
            unit_aliases[unit_group].pop(alias)
        print(f"'{unit_type}' was removed from '{unit_group}'")
    try:
        units_backup = units.copy()
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
        units = units_backup


def add_temp_type(unit_group, unit_type, action, temp_factor=None, temp_offset=None) -> None:
    """Handles all logic for adding temperature units"""
    global units
    if action == "add":
        if temp_factor == None:
            temp_factor: str = input(f"Enter conversion factor to base unit '{base_units[unit_group]}' of 'temperature' group: ").strip().lower()
        if temp_offset == None:
            temp_offset: str = input(f"Enter offset value to base unit '{base_units[unit_group]}' of 'temperature' group: ").strip().lower()
        if not temp_factor or not temp_offset:
            raise ValueError("You can't leave a field empty!")
        try:
            temp_factor = float(temp_factor)
            temp_offset = float(temp_offset)
        except:
            raise ValueError("Invalid value!")
        if temp_factor <= 0:
            raise ValueError("Conversion factor must be positive!")
        units[unit_group][unit_type] = [temp_factor, temp_offset]
        print(f"A new unit type was added on temperature group: {unit_type} = [{temp_factor}, {temp_offset}]")
    else:
        raise TypeError("Invalid action!")

    try:
        units_backup = units.copy()
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
        units = units_backup
    return


def add_new_group(unit_group) -> None:
    """Creates a new unit group, with a base unit"""
    global units
    global base_units
    new_base_unit: str = input(f"You are creating a new group. Enter the base unit for '{unit_group}' group: ").strip().lower()
    if not new_base_unit:
        raise ValueError("You need to specify the base unit to create a new group")
    elif new_base_unit == "quit":
        print("Action cancelled!")
        return
    units[unit_group] = {}
    units[unit_group][new_base_unit] = 1.0
    base_units[unit_group] = new_base_unit
    try:
        units_backup = units.copy()
        base_units_backup = base_units.copy()
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
        with open("base_units.json", "w") as file:
            json.dump(base_units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
        units = units_backup
        base_units = base_units_backup
        return

    print(f"You've just created a '{unit_group}' group, with '{new_base_unit}' as its base unit!")
    return 


def manage_aliases(unit_group=None, unit_type=None, action=None, alias=None):
    """Handles aliases, allowing users to add or remove aliases to/from an unit type"""
    global unit_aliases
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if unit_group not in units:
        raise KeyError(f"'{unit_group}' is not a valid group!")
    if unit_type is None:
        unit_type: str = resolve_aliases(unit_group, input(f"Enter unit type for '{unit_group}' group: ").strip().lower())
    if unit_type not in units[unit_group]:
        raise KeyError(f"'{unit_type}' is not a valid unit type for '{unit_group}' group!")
    all_aliases = [alias for alias in unit_aliases[unit_group] if unit_type == unit_aliases[unit_group].get(alias)]
    if action is None:
        action = input(f"Existed aliases for '{unit_type}': {all_aliases}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()
    if alias is None:
        alias = input(f"Which alias do you want to {action} {"to" if action == "add" else "from"} '{unit_type}'? ").strip().lower()
    if not action or action not in ["add", "remove"]:
        raise ValueError(f"Invalid action. Decide if you want to 'add' or 'remove' an alias for '{unit_type}'")
    if not alias:
        raise ValueError("You need to enter an alias before proceeding!")
    all_group_aliases = [alias for alias in unit_aliases[unit_group]]
    if alias in all_group_aliases and action == "add":
        raise ValueError(f"'{alias}' is already being used!")
    if alias in base_units:
        raise KeyError("You can't use the name of an unit group as an alias!")
    if alias in units[unit_group]:
        raise KeyError("You can't use the name of an unit type as an alias")
    if action == "add":
        if alias in unit_aliases[unit_group]:
            raise ValueError(f"{alias} is already an alias of {unit_type}")
        unit_aliases[unit_group][alias] = unit_type
        print(f"Alias successfully added! New alias for '{unit_type}': {alias}")
    elif action == "remove":
        if alias not in unit_aliases[unit_group]:
            raise ValueError(f"{alias} is not an alias of {unit_type}")
        unit_aliases[unit_group].pop(alias) 
        print(f"{alias} successfully removed from '{unit_type}'!")

    try:
        unit_aliases_backup = unit_aliases.copy()
        with open("unit_aliases.json", "w") as file:
            json.dump(unit_aliases, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to all_aliases.json")
        unit_aliases = unit_aliases_backup


def change_base_unit(unit_group=None, new_base_unit=None):
    """Allows change of base unit for a specific unit group"""
    global units
    global base_units
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if unit_group not in units:
        raise KeyError(f"{unit_group} is not a valid group!")
    if new_base_unit is None:
        print(f"All unit types for '{unit_group}' group: " + ", ".join(units[unit_group].keys()))
        new_base_unit: str = resolve_aliases(unit_group, input(f"Enter unit type for '{unit_group}' group: ").strip().lower())
    if not new_base_unit:
        raise ValueError("Enter an unit type before proceeding!")    
    elif new_base_unit not in units[unit_group]:
        raise KeyError(f"'{new_base_unit}' is not an unit type for '{unit_group}' group")
    elif new_base_unit == base_units[unit_group]:
        raise ValueError(f"'{new_base_unit}' is already the current base unit for '{unit_group}' group")

    refactor_value(unit_group, new_base_unit)
    base_units[unit_group] = new_base_unit

    try:
        units_backup = units.copy()
        base_units_backup = base_units.copy()
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
        with open("base_units.json", "w") as file:
            json.dump(base_units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
        units = units_backup
        base_units = base_units_backup
        return

    print(f"You've just changed the base unit from '{unit_group}' group, to '{new_base_unit}'!")
    return


def refactor_value(unit_group, new_base_unit):
    """Helper function that allows"""
    if unit_group == "temperature":
        new_base_factor, new_base_offset = units[unit_group][new_base_unit]
        if new_base_factor == 0:
            raise ZeroDivisionError("Can't dive by zero!")
        for unit_type in units[unit_group]:
            factor, offset = units[unit_group][unit_type]
            factor /= new_base_factor
            offset -= new_base_offset
            units[unit_group][unit_type] = [factor, offset]
    else:
        if units[unit_group][new_base_unit] == 0:
            raise ZeroDivisionError("Can't dive by zero!")
        for unit_type in units[unit_group]:
            units[unit_group][unit_type] /= units[unit_group][new_base_unit]
    return


if __name__ == "__main__":
    main()