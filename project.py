import json
import re
import sys


# Import dictionaries
try:
    # Dictionary with all units available
    with open("units.json", "r") as file:
        units = json.load(file)
    # Dictionary of base units for each group
    with open("base_units.json", "r") as file:
        base_units = json.load(file)
except FileNotFoundError:
    sys.exit("Error: file not found!")
except json.JSONDecodeError:
    sys.exit("Error: file if corrupted!")


def main() -> None:
    print_introductory_messages()
    get_action()


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
            raise ValueError("Amount cannot be empty")
        if not re.search(r"^-?\d+(\.\d+)?$", amount):
            raise ValueError("Invalid amount! Please, insert integer or decimals!")
        # Prevents negative value for "Kelvin"
        if from_type == "kelvin":
            if float(amount) < 0:
                raise ValueError("Kelvin temperature cannot be negative!")
        return float(amount)


def converter(amount, unit_group, from_type, to_type) -> float:
    """Convert one value to another"""
    # Separates logic for converting temperature units
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