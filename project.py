import argparse
import calendar
import json
import re
import sys

from datetime import datetime, timedelta
from math import fabs

from unit_converter.data_manager import load_data, add_to_log, refactor_value, save_data, zero_division_checker
from unit_converter.utils import resolve_aliases, parse_time_input, parse_date_input, get_seconds, format_value, calculate_leap_years, validate_date, get_days_from_month, get_index_from_month, gets_days_from_index


def main() -> None:
    # Handles data loading and validation
    try:
        # Initiates a 'ConversionData' object
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

    # Parses arguments and calls its respective function
    parsed_args = parser.parse_args(formatted_args[1:])  # Skips first argument (program's name)
    if parsed_args.command in ["groups", "g"]:
        print_groups(data)
    elif parsed_args.command in ["history", "h"]:
        print_history(data, parsed_args.limit)
    elif parsed_args.command in ["types", "t"]:
        unit_group = parsed_args.unit_group.lower()
        print_types(data, unit_group)
    elif parsed_args.command in ["convert", "c"]:
        unit_group = parsed_args.unit_group.lower()
        if unit_group == "time":
            lower_args = [arg.lower() for arg in parsed_args.args]
            converter_time(data, unit_group, *lower_args)
        else:
            if len(parsed_args.args) not in [2, 3]:
                raise ValueError("Invalid format for non-time conversion! Usage: <from_type> <to_type> <amount>")
            from_type = resolve_aliases(data, unit_group, parsed_args.args[0].lower())
            to_type = resolve_aliases(data, unit_group, parsed_args.args[1].lower())
            try:
                amount = float(parsed_args.args[2]) if len(parsed_args.args) == 3 else 1.0
                new_value = converter(data, amount, unit_group, from_type, to_type)
                print(f"{format_value(amount)} {from_type} = {format_value(new_value)} {to_type}")
            except (ValueError, TypeError, KeyError) as e:
                raise ValueError(f"Error: {str(e)}")
    elif parsed_args.command in ["add", "a"]:
        unit_group = parsed_args.unit_group.lower()
        unit_type = parsed_args.unit_type.lower()
        action = parsed_args.action.lower()
        # Adds temperature type
        if unit_group == "temperature":
            if parsed_args.factor is None or parsed_args.offset is None:
                raise ValueError("Adding temperature type requires --factor and --offset")
            add_temp_type(data, unit_group, unit_type, action, parsed_args.factor, parsed_args.offset)
        # Adds unit type for existed group
        elif unit_group in data.units:
            if parsed_args.value is None:
                raise ValueError("Adding non-temperature type requires a value")
            manage_type(data, unit_group, unit_type, parsed_args.value, action)
        # Creates new group and new type
        else:
            add_new_group(data, unit_group)
    elif parsed_args.command in ["aliases", "al"]:
        unit_group = parsed_args.unit_group.lower()
        unit_type = parsed_args.unit_type.lower()
        action = parsed_args.action.lower()
        alias = parsed_args.alias.lower()
        manage_aliases(data, unit_group, unit_type, action, alias)
    elif parsed_args.command in ["change-base", "cb"]:
        unit_group = parsed_args.unit_group.lower()
        new_base_unit = parsed_args.new_base_unit.lower()
        change_base_unit(data, unit_group, new_base_unit)


def print_introductory_messages() -> None:
    """Prints introductory messages and instructions"""
    print("Welcome to unit converter!")
    print("To check all group of units available, enter 'groups'")
    print("To check all types for a specific group, enter 'types'")
    print("To convert an unit, enter 'convert'")
    print("To add a new unit group or a new unit type, enter 'add'")
    print("Quit anytime by entering 'quit' or by pressing ctrl+d or ctrl+c", end="\n\n")


def get_action(data) -> None:
    while True:
        try:
            action: str = input("Let's begin! What do you want to do? ").strip().lower()
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
            elif action in ["add", "a"]:
                manage_type(data)
                continue
            elif action in ["aliases", "al"]:
                manage_aliases(data)
                continue
            elif action in ["change-base", "cb"]:
                change_base_unit(data)
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
        unit_group: str = get_unit_group(data)
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

    print("Units: " + ", ".join(formatted_output))


def conversion_logic(data) -> None:
    """Handles all logic of unit conversion"""
    unit_group: str = get_unit_group(data)
    if unit_group == "time":
        print_time_instructions()
        time_input = input("Enter time conversion: ").strip().lower()
        if not time_input:
            raise ValueError("Time conversion can't be empty! Enter an expression!")
        converter_time(data, unit_group, *time_input.split())
        return
    from_type, to_type = get_converter_units(data, unit_group)
    amount: float = get_amount(from_type)
    new_value: str = converter(data, amount, unit_group, from_type, to_type)

    print(f"{format_value(amount)} {from_type} = {format_value(new_value)} {to_type}")   


def get_unit_group(data) -> str:
    """Gets unit group"""
    unit_group: str = input("Unit group: ").strip().lower()
    if not unit_group:
        raise ValueError("Unit group cannot be empty!")
    if unit_group not in data.units:
        raise KeyError(f"{unit_group} is not a valid group!")
    return unit_group


def get_converter_units(data, unit_group) -> tuple[str, str]:
    """Gets types of units"""
    from_type: str = resolve_aliases(data, unit_group, input("From: ").strip().lower())
    to_type: str = resolve_aliases(data, unit_group, input("To: ").strip().lower())
    if not from_type or not to_type:
        raise ValueError("Unit type cannot be empty!")
    if from_type not in data.units[unit_group] or to_type not in data.units[unit_group]:
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


def converter(data, amount, unit_group, from_type, to_type) -> float:
    """Convert one value to another"""
    # Separates conversion logic when dealing with temperature
    if unit_group == "temperature":
        new_temp = converter_temp(data, amount, unit_group, from_type, to_type)
        # Adds to log file
        add_to_log(data, unit_group=unit_group, from_type=from_type, to_type=to_type, amount=amount, new_value=new_temp)
        return new_temp   
    
    zero_division_checker(float(data.units[unit_group][to_type]))
    new_value = amount * (data.units[unit_group][from_type]/data.units[unit_group][to_type])
    # Adds to log file
    add_to_log(data, unit_group=unit_group, from_type=from_type, to_type=to_type, amount=amount, new_value=new_value)

    return new_value


def converter_temp(data, amount, unit_group, from_type, to_type) -> float:
    """Handles conversion for temperature units"""
    # Get's conversion factor and offset for temperature calculation
    factor_from, offset_from = data.units[unit_group][from_type]
    factor_to, offset_to = data.units[unit_group][to_type]
    if from_type == "celsius":
        return (amount * factor_to) + offset_to
    zero_division_checker(factor_from)
    temp_in_celsius = (amount - offset_from) / factor_from
    if to_type == "celsius":
        return temp_in_celsius
    return (temp_in_celsius * factor_to) + offset_to


def converter_time(data, unit_group, *args) -> None:
    """Handles conversion for time units"""    
    if len(args) == 2:
        try:
            from_time, factor_time = args
        except ValueError:
            raise ValueError("Invalid format for date and time conversion!")
        converter_time_2args(data, unit_group, from_time, factor_time)
        return
    
    elif len(args) == 3:
        try:
            from_time, to_time, factor_time = args
        except ValueError:
            raise ValueError("Invalid format for date and time conversion!")
        converter_time_3args(data, unit_group, from_time, to_time, factor_time)
        return

    # E.g. 5 years 10 months 10 days 8 hours 56 minutes seconds
    elif len(args) % 2 != 0 and len(args) > 2:
        target_type = args[-1]  # Unit type that all args will be converted to
        if target_type not in data.units[unit_group]:
            raise ValueError(f"'{target_type}' is not a type for '{unit_group}' group!")
        zero_division_checker(data.units[unit_group][target_type])
        formatted_value = []
        total_seconds = 0
        for number, unit_type in zip(args[0::2], args[1::2]):
            try:
                number = float(number)
            except:
                raise ValueError(f"'{number}' is an invalid amount!")            
            if resolve_aliases(data, unit_group, unit_type) not in data.units[unit_group]:
                raise ValueError(f"'{unit_type}' is not a type for '{unit_group}' group!")
            
            total_seconds += number * data.units[unit_group][resolve_aliases(data, unit_group, unit_type)]
            formatted_value.append((format_value(number), unit_type))
        
        new_time = total_seconds / data.units[unit_group][target_type]

        print(f"{' '.join(f'{num} {unit}' for num, unit in formatted_value)} = {format_value(new_time)} {target_type}")
        add_to_log(
            data,
            unit_group=unit_group, 
            from_time=" ".join(f"{num} {unit}" for num, unit in formatted_value), 
            to_time=target_type, 
            new_time=new_time, 
            is_time_convertion=True
        )

    else:
        raise ValueError("Invalid format for date and time conversion!")


def converter_time_3args(data, unit_group, from_time, to_time, factor_time):
    # E.g. seconds minutes 10
    if resolve_aliases(data, unit_group, from_time) in data.units[unit_group] and resolve_aliases(data, unit_group, to_time) in data.units[unit_group]:
        from_time = resolve_aliases(data, unit_group, from_time)
        to_time = resolve_aliases(data, unit_group, to_time)
        try:
            factor_time = float(factor_time)
        except ValueError:
            raise ValueError("Enter a valid value for conversion!")            
        total_seconds = factor_time * data.units[unit_group][from_time]
        zero_division_checker(data.units[unit_group][to_time])
        new_time = total_seconds / data.units[unit_group][to_time]
        print(f"{format_value(factor_time)} {from_time} = {format_value(new_time)} {to_time}")

    else:
        factor_time = resolve_aliases(data, unit_group, factor_time)
        if factor_time not in data.units[unit_group]:
            raise KeyError(f"Unit type '{factor_time}' not found in '{unit_group}' group!")
        zero_division_checker(data.units[unit_group][factor_time])
        
        # E.g. 17h:28m:36s 04h:15m:22s seconds
        if parse_time_input(from_time) is not None and parse_time_input(to_time) is not None:
            new_from_time = parse_time_input(from_time)
            new_to_time = parse_time_input(to_time)
            new_time = fabs((new_from_time - new_to_time) / data.units[unit_group][factor_time])
            print(f"There are {format_value(new_time)} {factor_time} between {from_time} and {to_time}")
        
        # E.g. JAN NOV minutes
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
                new_time = days
            else:
                total_seconds = (timedelta(seconds=days * data.units[unit_group]["days"])).total_seconds()
                zero_division_checker(data.units[unit_group][factor_time])
                new_time = total_seconds / data.units[unit_group][factor_time]
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
                raise ValueError("Invalid date!")
            from_total_days = from_years * year_duration
            to_total_days = to_years * year_duration
            for month in range(1, from_months):
                from_total_days += gets_days_from_index(data, str(month))
            for month in range(1, to_months):
                to_total_days += gets_days_from_index(data, str(month))
            from_total_days += from_days
            to_total_days += to_days
            
            leap_years = calculate_leap_years(from_years, from_months, from_days, to_years, to_months, to_days)
            total_days = abs((from_total_days - to_total_days)) + 1 + leap_years
            total_seconds = total_days * data.units[unit_group]["days"]
            new_time = total_seconds / data.units[unit_group][factor_time]        
            print(f"Between {from_time} and {to_time} there are {format_value(new_time)} {factor_time}")

        # Any other format is invalid!
        else:
            print("Invalid time conversion format!")
            return

    add_to_log(data, unit_group=unit_group, from_time=from_time, to_time=to_time, factor_time=factor_time, new_time=new_time, is_time_convertion=True)


def converter_time_2args(data, unit_group, from_time, factor_time):
    factor_time = resolve_aliases(data, unit_group, factor_time)
    if factor_time not in data.units[unit_group]:
        raise KeyError(f"Unit type '{factor_time}' not found in '{unit_group}' group!")      
    zero_division_checker(data.units[unit_group][factor_time])

    # E.g. 17h:28m:36s seconds
    if parse_time_input(from_time) is not None:
        total_seconds = parse_time_input(from_time)
        new_time = (total_seconds / data.units[unit_group][factor_time])
        print(f"There are {format_value(new_time)} {factor_time} in {from_time}")

    # E.g. JAN minutes
    elif from_time in data.all_months:
        days = get_days_from_month(data, from_time)
        total_seconds = days * data.units[unit_group]["days"]
        new_time = total_seconds / data.units[unit_group][factor_time]
        print(f"There are {format_value(new_time)} {factor_time} in {from_time}")

    # E.g. 2019-11-04 days
    elif parse_date_input(from_time) is not None:
        years, months, days = parse_date_input(from_time)
        total_seconds = get_seconds(data, unit_group, years, months, days)
        new_time = total_seconds / data.units[unit_group][factor_time]
        print(f"There are {format_value(new_time)} {factor_time} in {years} years, {months} months, {days} days")

    # Any other format is invalid!
    else:
        print("Invalid time conversion format!")
        return

    add_to_log(data, unit_group=unit_group, from_time=from_time, factor_time=factor_time, new_time=new_time, is_time_convertion=True)


def print_time_instructions():
    """Prints instructions for converting date and time units"""
    print("For date-time conversion, you can choose from different approaches for conversion:")
    print(" - From a specific unit to another. Usage: <unit_type> <unit_type> quantity")
    print(" - From a more complex time to another. Usage: HH:MM:SS HH:MM:SS <unit_type>")
    print(" - From one month to another. Usage: <month_name> <month_name> <unit_type>")
    print(" - From a date to another. Usage: YYYY-MM-DD YYYY-MM-DD <unit_type>")


def manage_type(data, unit_group=None, unit_type=None, value=None, action=None) -> None:
    """Handles all logic of adding new unit type"""
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if not unit_group:
        raise ValueError("Enter a group name before proceeding!")    
    elif unit_group not in data.units:
        add_new_group(data, unit_group)
        return
    if action is None:
        action = input(f"Existed types for '{unit_group}' group: {data.units[unit_group]}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()    
    if not action or action not in ["add", "remove"]:
        raise ValueError(f"Invalid action. Decide if you want to 'add' or 'remove' an alias for '{unit_type}'")
    elif action == "add":
        if unit_type is None:
            unit_type: str = input(f"Enter new type for '{unit_group}' group: ").strip().lower()
        if not unit_type:
            raise ValueError("You can't leave that field empty!")
        if unit_type in data.units:
            raise KeyError(f"'{unit_type}' is already an unit group name!")
        elif unit_type in data.units[unit_group]:
            raise ValueError(f"'{unit_type}' is already an unit type!")
        elif unit_type in data.unit_aliases[unit_group]: 
            raise ValueError(f"'{unit_type}' is already being used as an alias in '{unit_group}' group")
        if unit_group == "temperature":
            add_temp_type(data, unit_group, unit_type, action="add")
            return
        if value is None:
            value: str = input(f"Enter conversion factor to base unit '{data.base_units[unit_group]}' of '{unit_group}' group: ").strip().lower()
        if not value:
            raise ValueError("You can't leave that field empty!")
        try:
            value = float(value)
        except:
            raise ValueError("Invalid value!")
        data.units[unit_group][unit_type] = value
        print(f"A new unit type was added on '{unit_group}' group: {unit_type} = {value}")
    elif action == "remove":
        if unit_type is None:
            unit_type: str = input(f"Enter new type for '{unit_group}' group: ").strip().lower()
        if not unit_type:
            raise ValueError("You can't leave that field empty!")
        elif unit_type not in data.units[unit_group]:
            raise ValueError(f"'{unit_type}' is not an unit type in '{unit_group}' group!")
        elif unit_type == data.base_units[unit_group]:
            raise ValueError("Cannot remove base unit!")
        data.units[unit_group].pop(unit_type)
        aliases_to_remove = [alias for alias, unit in data.unit_aliases[unit_group] if unit == unit_type]
        for alias in aliases_to_remove:
            data.unit_aliases[unit_group].pop(alias)
        print(f"'{unit_type}' was removed from '{unit_group}'")
    save_data(data.units, "units")


def add_temp_type(data, unit_group, unit_type, action, temp_factor=None, temp_offset=None) -> None:
    """Handles all logic for adding temperature units"""
    if action == "add":
        if temp_factor == None:
            temp_factor: str = input(f"Enter conversion factor to base unit '{data.base_units[unit_group]}' of 'temperature' group: ").strip().lower()
        if temp_offset == None:
            temp_offset: str = input(f"Enter offset value to base unit '{data.base_units[unit_group]}' of 'temperature' group: ").strip().lower()
        if not temp_factor or not temp_offset:
            raise ValueError("You can't leave a field empty!")
        try:
            temp_factor = float(temp_factor)
            temp_offset = float(temp_offset)
        except:
            raise ValueError("Invalid value!")
        if temp_factor <= 0:
            raise ValueError("Conversion factor must be positive!")
        data.units[unit_group][unit_type] = [temp_factor, temp_offset]
        print(f"A new unit type was added on temperature group: {unit_type} = [{temp_factor}, {temp_offset}]")
    else:
        raise TypeError("Invalid action!")

    save_data(data.units, "units")

    return


def add_new_group(data, unit_group) -> None:
    """Creates a new unit group, with a base unit"""
    new_base_unit: str = input(f"You are creating a new group. Enter the base unit for '{unit_group}' group: ").strip().lower()
    if not new_base_unit:
        raise ValueError("You need to specify the base unit to create a new group")
    elif new_base_unit == "quit":
        print("Action cancelled!")
        return
    data.units[unit_group] = {}
    data.units[unit_group][new_base_unit] = 1.0
    data.base_units[unit_group] = new_base_unit
    
    save_data(data.units, "units")
    save_data(data.base_units, "base_units")    

    print(f"You've just created a '{unit_group}' group, with '{new_base_unit}' as its base unit!")
    return 


def manage_aliases(data, unit_group=None, unit_type=None, action=None, alias=None):
    """Handles aliases, allowing users to add or remove aliases to/from an unit type"""
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if unit_group not in data.units:
        raise KeyError(f"'{unit_group}' is not a valid group!")
    if unit_type is None:
        unit_type: str = resolve_aliases(data, unit_group, input(f"Enter unit type for '{unit_group}' group: ").strip().lower())
    if unit_type not in data.units[unit_group]:
        raise KeyError(f"'{unit_type}' is not a valid unit type for '{unit_group}' group!")
    all_aliases = [alias for alias in data.unit_aliases[unit_group] if unit_type == data.unit_aliases[unit_group].get(alias)]
    if action is None:
        action = input(f"Existed aliases for '{unit_type}': {all_aliases}. What do you want to do? (enter 'add' or 'remove') ").strip().lower()
    if alias is None:
        alias = input(f"Which alias do you want to {action} {"to" if action == "add" else "from"} '{unit_type}'? ").strip().lower()
    if not action or action not in ["add", "remove"]:
        raise ValueError(f"Invalid action. Decide if you want to 'add' or 'remove' an alias for '{unit_type}'")
    if not alias:
        raise ValueError("You need to enter an alias before proceeding!")
    all_group_aliases = [alias for alias in data.unit_aliases[unit_group]]
    if alias in all_group_aliases and action == "add":
        raise ValueError(f"'{alias}' is already being used!")
    if alias in data.base_units:
        raise KeyError("You can't use the name of an unit group as an alias!")
    if alias in data.units[unit_group]:
        raise KeyError("You can't use the name of an unit type as an alias")
    if action == "add":
        if alias in data.unit_aliases[unit_group]:
            raise ValueError(f"{alias} is already an alias of {unit_type}")
        data.unit_aliases[unit_group][alias] = unit_type
        print(f"Alias successfully added! New alias for '{unit_type}': {alias}")
    elif action == "remove":
        if alias not in data.unit_aliases[unit_group]:
            raise ValueError(f"{alias} is not an alias of {unit_type}")
        data.unit_aliases[unit_group].pop(alias) 
        print(f"{alias} successfully removed from '{unit_type}'!")

    data.unit_aliases = save_data(data.unit_aliases, "unit_aliases")


def change_base_unit(data, unit_group=None, new_base_unit=None):
    """Allows change of base unit for a specific unit group"""
    if unit_group is None:
        unit_group: str = input("Enter a group name: ").strip().lower()
    if unit_group not in data.units:
        raise KeyError(f"{unit_group} is not a valid group!")
    if new_base_unit is None:
        print(f"All unit types for '{unit_group}' group: " + ", ".join(data.units[unit_group].keys()))
        new_base_unit: str = resolve_aliases(data, unit_group, input(f"Enter unit type for '{unit_group}' group: ").strip().lower())
    if not new_base_unit:
        raise ValueError("Enter an unit type before proceeding!")    
    elif new_base_unit not in data.units[unit_group]:
        raise KeyError(f"'{new_base_unit}' is not an unit type for '{unit_group}' group")
    elif new_base_unit == data.base_units[unit_group]:
        raise ValueError(f"'{new_base_unit}' is already the current base unit for '{unit_group}' group")

    refactor_value(data, unit_group, new_base_unit)
    data.base_units[unit_group] = new_base_unit

    save_data(data.units, "units")
    save_data(data.base_units, "base_units")

    print(f"You've just changed the base unit from '{unit_group}' group, to '{new_base_unit}'!")
    return 


if __name__ == "__main__":
    main()