import argparse
import json
import re
import sys


# Imports dictionaries
try:
    # Opens dictionary with all units available
    with open("units.json", "r") as file:
        units = json.load(file)
    # Opens dictionary of base units for each group
    with open("base_units.json", "r") as file:
        base_units = json.load(file)
except FileNotFoundError:
    sys.exit("Error: file not found!")
except json.JSONDecodeError:
    sys.exit("Error: file if corrupted!")


def validate_dictionaries(units, base_units):
    """Validates dictionaries before entering the program"""
    # Ensures 'units.json' is a dictionary and it's not empty
    if not isinstance(units, dict) or not units:
        raise ValueError("'units.json' dictionary structure is corrupted!")
    # Ensures 'base_units.json' is a dictionary and it's not empty
    if not isinstance(base_units, dict) or not base_units:
        raise ValueError("'base_units.json' dictionary structure is corrupted!")
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

validate_dictionaries(units, base_units)

def main() -> None:
    # Handles argparse
    if len(sys.argv) > 1:
        handle_cli(sys.argv)
    print_introductory_messages()
    get_action()


def handle_cli(args):
    """Handles command-line instructions (CLI)"""
    # Convert command-line arguments to lowercase
    modified_args = args[:]  # Creates a copy of all command-line arguments
    
    

    # Adds description to program
    parser = argparse.ArgumentParser(prog="Unit Converter", description="Convert multiple types of units")
    subparser = parser.add_subparsers(dest="command", help="Available commands")
    
    # Convert command 
    convert_parser = subparser.add_parser("convert", help="Convert value from one type to another")
    convert_parser.add_argument("amount", type=float, help="Amount to convert")
    convert_parser.add_argument("unit_group", help="Unit group")
    convert_parser.add_argument("from_type", help="Source unit type")
    convert_parser.add_argument("to_type", help="Target unit type")

    # Add command
    add_parser = subparser.add_parser("add", help="Add new unit group/type")
    add_parser.add_argument("group", help="Unit group to add new type to")
    add_parser.add_argument("unit_type", help="New type to be added")
    add_parser.add_argument("value", type=float, nargs="?", help="Conversion factor to base unit (not used for temperature)")
    add_parser.add_argument("factor", type=float, nargs="?", help="Conversion factor to temperature's base unit")
    add_parser.add_argument("offset", type=float, nargs="?", help="Offset to temperature")

    # Groups command
    subparser.add_parser("groups", help="List all unit groups")

    # Types command
    types_parser = subparser.add_parser("types", help="List all types of units in a group")
    types_parser.add_argument("group", help="Unit group used to list unit types")

    # Parse arguments and call their respective functions
    parsed_args = parser.parse_args(args[:1])  # Skips first argument
    if parsed_args.command == "groups":
        print("Groups: " + ", ".join(units.keys()))
    elif parsed_args.command == "types":
        if parsed_args.group not in units:
            sys.exit(f"Error: '{parsed_args.group}' is not a invalid group")    
    elif parsed_args.command == "convert":
        try:
            new_value = converter(parsed_args.amount, parsed_args.unit_group, parsed_args.from_type, parsed_args.to_type)
            print(f"{parsed_args.amount} {parsed_args.from_type} = {format_value(new_value)} {parsed_args.to_type}")
        except (ValueError, KeyError, ZeroDivisionError) as e:
            sys.exit(f"Error: {e}")
    elif parsed_args.comman == "add":
        ...
    


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
            # Add logic to check action validity
            if action == "groups":
                print("Groups: " + ", ".join(units.keys()))
                continue
            elif action.endswith(".types"):
                group, _ = action.split(".")
                if group not in units:
                    raise KeyError(f"{group} is not a valid group!")
                print("Units: " + ", ".join(units[group].keys()))
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


def conversion_logic() -> None:
    """Handles all logic of unit conversion"""
    unit_group: str = get_unit_group()    
    from_type, to_type = get_converter_unit(unit_group)
    amount: float = get_amount(from_type)
    new_value: float = format_value(converter(amount, unit_group, from_type, to_type))

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
        converter_temp(amount, unit_group, from_type, to_type)
    if float(units[unit_group][to_type]) == 0:
        raise ZeroDivisionError("Can't divide by zero!")
    return amount * (units[unit_group][from_type]/units[unit_group][to_type])


def format_value(value: float) -> str:
    """Format converted value by allowing only 5 decimal values and elimitating all trailling zeroes"""
    formatted_value = f"{value:.5f}".rstrip("0").rstrip(".")
    # Adds '.0' if formatted value ended up with no decimal values
    if "." not in formatted_value:
        formatted_value += ".0"
    return formatted_value


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


def add_logic() -> None:
    """Handles all logic of adding new unit type"""
    group: str = input("Enter a group name: ").strip().lower()
    if not group:
        raise ValueError("Enter a group name before proceeding!")
    elif group not in units:
        add_new_group(group)
        return
    unit_type: str = input(f"Enter new type for {group} group: ").strip().lower()
    if group == "temperature":
        add_temp_logic(group, unit_type)
        return
    value: str = input(f"Enter conversion factor to base unit of {group} group ({base_units[group]}): ").strip().lower()
    if not unit_type or not value:
        raise ValueError("You can't leave a field empty!")
    elif unit_type in units[group]:
        raise KeyError(f"{unit_type} is already an unit type!")
    try:
        value = float(value)
    except:
        raise ValueError("Invalid value!")
    units[group][unit_type] = value
    print(f"A new unit type was added on {group} group: {unit_type} = {value}")
    try:
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")


def add_new_group(group) -> None:
    """Creates a new unit group, with a base unit"""
    while True:
        answer: str = input(f"You want to create a new unit group named {group}? ").strip().lower()
        if answer not in ["no", "n", "yes", "y"]:
            print("Invalid answer! Just enter 'yes' or 'no'!")
            continue
        if answer == "no" or answer == "n":
            print("Action cancelled!") 
            return 
        units[group] = {}
        new_base_unit: str = input("Group created! Now, enter the base unit for that group: ").strip().lower()
        if not new_base_unit:
            print("You can't leave that field empty! Enter a name for the base unit!")
            continue
        units[group][new_base_unit] = 1.0
        base_units[group] = new_base_unit
        try:
            with open("units.json", "w") as file:
                json.dump(units, file, indent=4)
            with open("base_units.json", "w") as file:
                json.dump(base_units, file, indent=4)
        except PermissionError:
            print("Error! You don't have permition to write to units.json!")

        print(f"You've just created a {group} group, with {new_base_unit} as its base unit!")
        return 


def add_temp_logic(group, unit_type) -> None:
    temp_factor: str = input(f"Enter conversion factor to base unit of 'temperature' group ({base_units[group]}): ").strip().lower()
    temp_offset: str = input(f"Enter offset value to base unit of 'temperature' group ({base_units[group]}): ").strip().lower()
    if not temp_factor or not temp_offset:
        raise ValueError("You can't leave a field empty!")
    elif unit_type in units[group]:
        raise KeyError(f"{unit_type} is already an unit type!")
    try:
        temp_factor = float(temp_factor)
        temp_offset = float(temp_offset)
    except:
        raise ValueError("Invalid value!")
    if temp_factor <= 0:
        raise ZeroDivisionError("Conversion factor cannot be zero!")
    units[group][unit_type] = [temp_factor, temp_offset]
            
    print(f"A new unit type was added on temperature group: {unit_type} = [{temp_factor}, {temp_offset}]")
    try:
        with open("units.json", "w") as file:
            json.dump(units, file, indent=4)
    except PermissionError:
        print("Error! You don't have permition to write to units.json!")
    return


if __name__ == "__main__":
    main()