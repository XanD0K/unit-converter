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
                    raise KeyError("That's not a valid group!")
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
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            continue


def conversion_logic() -> None:
    """Handles all logic of unit convertion"""  
    amount: float = get_amount()
    unit_group: str = get_unit_group()
    from_unit, to_unit = get_converter_unit(unit_group)
    new_value: float = converter(amount, unit_group, from_unit, to_unit)

    print(f"{amount} {from_unit} = {new_value:.05f} {to_unit}")


def get_amount() -> float:
    """Gets unit amount"""
    amount: str = input("Amount: ").strip()
    if not re.search(r"^\d+(\.\d+)?$", amount):
        raise ValueError("Invalid amount!")
    if not amount:
        raise ValueError("Amount cannot be empty")
    return float(amount)


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
    from_unit: str = input("From: ").strip().lower()
    to_unit: str = input("To: ").strip().lower()
    if not from_unit or not to_unit:
        raise ValueError("Unit type cannot be empty!")
    if from_unit not in units[unit_group] or to_unit not in units[unit_group]:
        raise KeyError("Invalid unit type!")
    return from_unit, to_unit


def converter(amount, unit_group, from_unit, to_unit) -> float:
    """Convert one value to another"""
    # Separate logic for converting temperature units
    if unit_group == "temperature":
        factor_from, offset_from = units[unit_group][from_unit]
        factor_to, offset_to = units[unit_group][to_unit]        
        if from_unit == "celsius":
            return (amount * factor_to) + offset_to        
        temp_in_celsius = (amount - offset_from) / factor_from        
        if to_unit == "celsius":
            return temp_in_celsius
        return (temp_in_celsius * factor_to) + offset_to

    if int(units[unit_group][to_unit]) == 0:
        raise ZeroDivisionError("Can't divide by zero!")
    return amount * (units[unit_group][from_unit]/units[unit_group][to_unit]) 


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
    value: str = input(f"Enter convertion factor to base unit of {group} group ({base_units[group]}): ").strip().lower()
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
    temp_factor: str = input(f"Enter convertion factor to base unit of 'temperature' group ({base_units[group]}): ").strip().lower()
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