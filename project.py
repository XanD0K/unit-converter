import argparse
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
    with open("days_to_month.json", "r") as file:
        days_to_month = json.load(file)
except FileNotFoundError:
    sys.exit("Error: file not found!")
except json.JSONDecodeError:
    sys.exit("Error: file if corrupted!")


def validate_dictionaries(units, base_units, conversion_log):
    """Validates dictionaries before entering the program"""
    # Ensures 'units.json' is a dictionary and it's not empty
    if not isinstance(units, dict) or not units:
        raise ValueError("'units.json' dictionary structure is corrupted!")
    # Ensures 'base_units.json' is a dictionary and it's not empty
    if not isinstance(base_units, dict) or not base_units:
        raise ValueError("'base_units.json' dictionary structure is corrupted!")
    if not isinstance(conversion_log, list):
        raise ValueError("'convert_history' dictionary structure is corrupted!")
    if not isinstance(days_to_month, dict):
        raise ValueError("'days_to_month' dictionary structure is corrupted!")
    for key in units:
        # Ensures every key in 'units.json' is also a dictionary
        if not isinstance(units[key], dict):
            raise ValueError(f"'units.json' disctionary is corrupted! Its '{units[key]}' key should also be a dictionary!")
        # Ensures every group in 'units.json' is also a group in 'base_units.json'
        if key not in base_units.keys():
            raise ValueError(f"Dictionaries don't match! '{key}' should also be a key in 'base_units.json' dictionary!")
        # Ensures base unit for each group is correctly define in 'units.json'
        if base_units[key] not in units[key]:
            raise ValueError(f"The base unit '{base_units[key]}' for {key} group is not present on 'units.json' dictionary!")

validate_dictionaries(units, base_units, conversion_log)


def main() -> None:
    # Handles command-line arguments
    try:
        if len(sys.argv) > 1:
            handle_cli(sys.argv)
            sys.exit(0)  # Exits program after command-line execution
    except (ValueError, KeyError, ZeroDivisionError) as e:
        print(f"Error: {e}")
        sys.exit(1) # Exits the program if any error happens
    # Access the program without command lines
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
    # Convert command 
    convert_parser = subparser.add_parser("convert", aliases=["c"], help="Convert value from one type to another")
    convert_parser.add_argument("unit_group", help="Unit group")
    convert_parser.add_argument("from_type", help="Source unit type")
    convert_parser.add_argument("to_type", help="Target unit type")
    convert_parser.add_argument("amount", type=float, help="Amount to convert")
    # Add command
    add_parser = subparser.add_parser("add", aliases=["a"], help="Add new unit group/type")
    add_parser.add_argument("unit_group", help="Unit group to add new type to")
    add_parser.add_argument("unit_type", help="New type to be added")
    add_parser.add_argument("value", type=float, nargs="?", help="Conversion factor to base unit (not used for temperature)")
    add_parser.add_argument("--factor", type=float, help="Conversion factor to temperature's base unit")
    add_parser.add_argument("--offset", type=float, help="Offset to temperature")
    # Groups command
    subparser.add_parser("groups", aliases=["g"], help="List all unit groups")
    # Types command
    types_parser = subparser.add_parser("types", aliases=["t"], help="List all types of units in a group")
    types_parser.add_argument("unit_group", help="Unit group used to list unit types")
    # History command
    history_parser = subparser.add_parser("history", aliases=["h"], help="List conversion history (default=10)")
    history_parser.add_argument("--limit", "-l", type=int, default=10, help="Number of conversion entries that will be printed")

    # Parses arguments
    parsed_args = parser.parse_args(formatted_args[1:])  # Skips first argument
    # Lowercases arguments
    if parsed_args.command in ["types", "t"]:
        parsed_args.unit_group = parsed_args.unit_group.lower()
    elif parsed_args.command in ["convert", "c"]:
        parsed_args.unit_group = parsed_args.unit_group.lower()
        parsed_args.from_type = parsed_args.from_type.lower()
        parsed_args.to_type = parsed_args.to_type.lower()
    elif parsed_args.command in ["add", "a"]:
        parsed_args.unit_group = parsed_args.unit_group.lower()
        parsed_args.unit_type = parsed_args.unit_type.lower()
    
    # Calls argument respective function
    if parsed_args.command in ["groups", "g"]:
        print_groups()
    elif parsed_args.command in ["history", "h"]:
        print_history(parsed_args.limit)
    elif parsed_args.command in ["types", "t"]:
        print_types(parsed_args.unit_group)
    elif parsed_args.command in ["convert", "c"]:
        new_value = converter(parsed_args.amount, parsed_args.unit_group, parsed_args.from_type, parsed_args.to_type)
        print(f"{parsed_args.amount} {parsed_args.from_type} = {format_value(new_value)} {parsed_args.to_type}")
    elif parsed_args.command in ["add", "a"]:
        # Adds temperature type
        if parsed_args.unit_group == "temperature":
            if parsed_args.factor is None or parsed_args.offset is None:
                raise ValueError("Adding temperature type requires --factor and --offset")
            add_temp_logic(parsed_args.unit_group, parsed_args.unit_type, parsed_args.factor, parsed_args.offset)
        # Adds unit type for existed group
        elif parsed_args.unit_group in units:
            if parsed_args.value is None:
                raise ValueError("Adding non-temperature type requires a value")
            add_logic(parsed_args.unit_group, parsed_args.unit_type, parsed_args.value)
        # Creates new group and new type
        else:
            add_new_group(parsed_args.unit_group)

def print_introductory_messages() -> None:
    """Prints introductory messages and instructions"""
    print("Welcome to unit converter!")
    print("To check all group of units available, enter 'groups'")
    print("To check all types for a specific group, enter '<group_name>.types'")
    print("To convert an unit, enter 'convert'")
    print("To add a new unit group or a new unit type, enter 'add'")
    print("Quit anytime by entering 'quit' or by pressing ctrl+d or ctrl+c", end="\n\n")


def get_action() -> None:
    while True:
        try:
            action: str = input("Let's begin! What do you want to do? ").strip().lower()
            # Adds logic to check action validity
            if action == "groups":
                print_groups()
                continue
            elif action == "history":
                print_history()
                continue
            elif action.endswith(".types"):
                unit_group, _ = action.split(".")
                print_types(unit_group)
                continue
            elif action == "convert":
                conversion_logic()
                continue
            elif action == "add":
                add_logic()
                continue
            elif action == "quit":
                sys.exit("Bye!")
            else:
                raise ValueError("That's not a valid action!")
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
        print(f"{entry["amount"]} {entry["from_type"]} = {format_value(entry["result"])} {entry["to_type"]} (Group: {entry["unit_group"]})")


def print_types(unit_group) -> None:
    """Prints all unit types for a specific unit group"""
    if unit_group not in units:
        raise KeyError(f"{unit_group} is not a valid group!")
    print("Units: " + ", ".join(units[unit_group].keys()))


def conversion_logic() -> None:
    """Handles all logic of unit conversion"""
    unit_group: str = get_unit_group()
    if unit_group == "time":
        converter_time(unit_group)
        return
    from_type, to_type = get_converter_unit(unit_group)
    amount: float = get_amount(from_type)
    new_value: str = format_value(converter(amount, unit_group, from_type, to_type))

    print(f"{amount} {from_type} = {new_value} {to_type}")   


def get_unit_group() -> str:
    """Gets unit group"""
    unit_group: str = input("Unit group: ").strip().lower()
    if not unit_group:
        raise ValueError("Unit group cannot be empty!")
    if unit_group not in units:
        raise KeyError("Invalid unit group!")
    return unit_group


def get_converter_unit(unit_group) -> tuple[str, str]:
    """Gets types of units user is convertind from and to"""
    from_type: str = input("From: ").strip().lower()
    to_type: str = input("To: ").strip().lower()
    if not from_type or not to_type:
        raise ValueError("Unit type cannot be empty!")
    if from_type not in units[unit_group] or to_type not in units[unit_group]:
        raise KeyError("Invalid unit type!")
    return from_type, to_type


def get_amount(from_type) -> float:
    """Gets unit amount"""
    while True:
        amount: str = input("Amount: ").strip()
        if not amount:
            print("Amount cannot be empty")
            continue
        # Ensures amount is a number
        elif not re.search(r"^-?\d+(\.\d+)?$", amount):
            print("Invalid amount! Please, insert integer or decimals! (e.g. 10 or 10.0)")
            continue
        elif float(amount) < 0:
            # Prevents negative value for "Kelvin"
            if from_type == "kelvin":
                raise ValueError("Kelvin temperature cannot be negative!")
            while True:
                # Ensures user really want convert negative value
                answer: str = input("WARNING! Negative values might not have physical meanings! Proceed anyway? ").strip().lower()
                if answer not in ["yes", "y", "no", "n"]:
                    print("Invalid answer! Just enter 'yes' or 'no'!")
                    continue
                if answer == "no" or answer == "n":
                    print("Action cancelled!")
                    break
                return float(amount)
            continue
        break
    return float(amount)


def converter(amount, unit_group, from_type, to_type) -> float:
    """Convert one value to another"""
    # Separates conversion logic when dealing with temperature
    if unit_group == "temperature":
        new_temp = converter_temp(amount, unit_group, from_type, to_type)
        # Adds to log file
        add_to_log(unit_group, from_type, to_type, amount, new_temp)
        return new_temp   
    if float(units[unit_group][to_type]) == 0:
        raise ZeroDivisionError("Can't divide by zero!")

    new_value = amount * (units[unit_group][from_type]/units[unit_group][to_type])
    # Adds to log file
    add_to_log(unit_group, from_type, to_type, amount, new_value)

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


def converter_time(unit_group) -> float:
    """Handles conversion for time units"""
    print_time_instructions()
    while True:
        time_input = input("Enter time conversion: ").strip().lower()
        try:            
            from_time, to_time, factor_time = time_input.split(" ")
        except ValueError:
            print("Enter a valid format! Read previous instructions!")            
            continue

        # E.g. seconds minutes 10
        if from_time in units[unit_group] and to_time in units[unit_group]:
            try:
                factor_time = float(factor_time)
            except ValueError:
                print("Enter a valid value for conversion!")
                continue
            else:
                total_seconds = timedelta(seconds=factor_time * units[unit_group][from_time]).total_seconds()
                new_time = total_seconds / units[unit_group][to_time]
                print(f"{factor_time} {from_time} = {new_time} {to_time}")
                return

        # E.g. 17:28:36 04:15:22 seconds
        elif parse_time_input(from_time) is not None and parse_time_input(to_time) is not None:
            if factor_time not in units[unit_group]:
                print(f"{factor_time} is not a valid unit type!")
                continue
            new_from_time = parse_time_input(from_time)
            new_to_time = parse_time_input(to_time)
            new_time = fabs((new_from_time - new_to_time) / units[unit_group][factor_time])
            print(f"There are {new_time} {factor_time} between {from_time} and {to_time}")
            return
        # E.g. JAN NOV minutes
        elif from_time in days_to_month and to_time in days_to_month:
            if not factor_time not in units[unit_group]:
                print(f"{factor_time} is not a valid unit type!")
                continue
            from_datetime = datetime(2023, days_to_month[from_time], 1)
            to_datetime = datetime(2023, days_to_month[to_time], 1) if days_to_month[to_time] > days_to_month[from_time] else datetime(2024, days_to_month[to_time], 1)
            days = abs((from_datetime - to_datetime)).days
            if factor_time == "days":
                print(f"Between {from_time} and {to_time} there are {days} {factor_time}")
                return
            total_seconds = (timedelta(seconds=days * units[unit_group]["days"])).total_seconds()
            new_time = total_seconds / units[unit_group][factor_time]
            print(f"Between {from_time} and {to_time} there are {new_time} {factor_time}")
            return
        
        # E.g. 2019-11-04 2056-04-28 days
        elif parse_date_input(from_time) is not None and parse_date_input(to_time) is not None:
            if not factor_time in units[unit_group]:
                print(f"{factor_time} is not a valid unit type!")
                continue            
            new_from_time = parse_date_input(from_time)
            new_to_time = parse_date_input(to_time)
            delta = abs(new_from_time - new_to_time)
            total_seconds = delta.total_seconds()
            if factor_time == "seconds":
                print(f"Between {from_time} and {to_time} there are {new_time} {factor_time}")
                return
            new_time = total_seconds / units[unit_group][factor_time]
            print(f"Between {from_time} and {to_time} there are {new_time} {factor_time}")
            return

def print_time_instructions():
    print("For date-time conversion, you can choose from different approaches for conversion:")
    print(" - From a specific unit to another. Usage: <unit_type> <unit_type> quantity")
    print(" - From a more complex time to another. Usage: HH:MM:SS HH:MM:SS <unit_type>")
    print(" - From one month to another. Usage: <month_name> <month_name> <unity_type>")
    print(" - From a date to another. Usage: YYYY-MM-DD YYYY-MM-DD <unit_type>")


def parse_time_input(time_str):
    if matches := re.search(r"^(?:(\d{1,2}):)?(?:(\d{1,2}):)?(\d{1,2})?$", time_str):
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


def parse_date_input(time_str):
    if matches := re.search(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", time_str):
        year, month, day = int(matches.group(1)), int(matches.group(2)), int(matches.group(3))
        return datetime(year, month, day)
    return None


def add_to_log(unit_group, from_type, to_type, amount, new_value) -> None:
    """Adds successfully converted value to log file (conversion_log.json)"""
    entry = {
        "unit_group": unit_group,
        "from_type": from_type,
        "to_type": to_type,
        "amount": amount,
        "result": float(new_value)
    }
    conversion_log.append(entry)
    try:
        with open("conversion_log.json", "w") as file:
            json.dump(conversion_log, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to conversion_log.json!")


def format_value(value: float) -> str:
    """Format converted value by allowing only 5 decimal values and elimitating all trailling zeroes"""
    formatted_value = f"{value:.5f}".rstrip("0").rstrip(".")
    # Adds '.0' if formatted value ended up with no decimal values
    if "." not in formatted_value:
        formatted_value += ".0"
    return formatted_value


def add_logic(unit_group=None, unit_type=None, value=None) -> None:
    """Handles all logic of adding new unit type"""
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if not unit_group:
        raise ValueError("Enter a group name before proceeding!")
    elif unit_group not in units:
        add_new_group(unit_group)
        return
    if unit_type is None:
        unit_type: str = input(f"Enter new type for {unit_group} group: ").strip().lower()
    if unit_group == "temperature":
        add_temp_logic(unit_group, unit_type)
        return
    if value is None:
        value: str = input(f"Enter conversion factor to base unit of {unit_group} group ({base_units[unit_group]}): ").strip().lower()
    if not unit_type or not value:
        raise ValueError("You can't leave a field empty!")
    elif unit_type in units[unit_group]:
        raise KeyError(f"{unit_type} is already an unit type!")
    try:
        value = float(value)
    except:
        raise ValueError("Invalid value!")
    units[unit_group][unit_type] = value
    print(f"A new unit type was added on {unit_group} group: {unit_type} = {value}")
    try:
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")


def add_new_group(unit_group) -> None:
    """Creates a new unit group, with a base unit"""
    while True:
        answer: str = input(f"You want to create a new unit group named {unit_group}? ").strip().lower()
        if answer not in ["no", "n", "yes", "y"]:
            print("Invalid answer! Just enter 'yes' or 'no'!")
            continue
        if answer == "no" or answer == "n":
            print("Action cancelled!") 
            return 
        units[unit_group] = {}
        new_base_unit: str = input("Group created! Now, enter the base unit for that group: ").strip().lower()
        if not new_base_unit:
            print("You can't leave that field empty! Enter a name for the base unit!")
            continue
        units[unit_group][new_base_unit] = 1.0
        base_units[unit_group] = new_base_unit
        try:
            with open("units.json", "w") as file:
                json.dump(units, file, indent=4)
            with open("base_units.json", "w") as file:
                json.dump(base_units, file, indent=4)
        except PermissionError:
            print("Error! You don't have permition to write to units.json!")

        print(f"You've just created a {unit_group} group, with {new_base_unit} as its base unit!")
        return 


def add_temp_logic(unit_group, unit_type, temp_factor=None, temp_offset=None) -> None:
    if temp_factor == None:
        temp_factor: str = input(f"Enter conversion factor to base unit of 'temperature' group ({base_units[unit_group]}): ").strip().lower()
    if temp_offset == None:
        temp_offset: str = input(f"Enter offset value to base unit of 'temperature' group ({base_units[unit_group]}): ").strip().lower()
    if not temp_factor or not temp_offset:
        raise ValueError("You can't leave a field empty!")
    elif unit_type in units[unit_group]:
        raise KeyError(f"{unit_type} is already an unit type!")
    try:
        temp_factor = float(temp_factor)
        temp_offset = float(temp_offset)
    except:
        raise ValueError("Invalid value!")
    if temp_factor <= 0:
        raise ZeroDivisionError("Conversion factor cannot be zero!")
    units[unit_group][unit_type] = [temp_factor, temp_offset]
            
    print(f"A new unit type was added on temperature group: {unit_type} = [{temp_factor}, {temp_offset}]")
    try:
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
    return


if __name__ == "__main__":
    main()