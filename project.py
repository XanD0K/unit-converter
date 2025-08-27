import re
import sys

# Get units dictionary from 'units.py' file
from units import units

def main():
    print("Welcome to unit converter!")
    print("To check all group of units available, enter 'groups'")
    print("To check all types for a specific group, enter '<group_name>.types'")
    print("To convert an unit, enter 'convert'")
    print("To add a new unit group or a new unit type, enter 'add'")
    print("Quit anytime by entering 'quit' or by pressing ctrl+d or ctrl+c", end="\n\n")

    while True:
        try:
            action = input("Let's begin! What do you want to do? ").strip().lower()
            # Add logic to check action validity
            if action == "groups":
                print(f"Groups: {units.keys()}")
                continue
            elif action.endswith(".types"):
                group, _ = action.split(".")
                print(f"Units: {units[group].keys()}")
                continue
            elif action == "convert":
                conversion_logic()
                continue
            elif action == "add":
                group = input("Enter a group name (if not existed, a new one will be created): ").strip().lower()
                unit_type = input(f"Enter new type for {group} group: ").strip().lower()
                value = input(f"Enter convertion factor to base unit: ").strip().lower()
                if not group or not unit_type or not value:
                    raise ValueError("You can't leave a field empty! Enter a value!")
                if group not in units:
                    units[group] = {}
                elif unit_type in units[group]:
                    raise KeyError(f"{unit_type} is already an unit type!")   
                try:
                    value = float(value)
                except:
                    raise ValueError("Invalid value!")             
                units[group][unit_type] = value
                print(f"A new unit type was added on {group} group: {unit_type} = {value}")
            elif action == "quit":
                sys.exit("Bye!")
        except (EOFError, KeyboardInterrupt):
            sys.exit("Bye!")
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            continue


def conversion_logic():
    """Handles all logic if user decides do convert an unit"""
    try:
        amount: float = get_amount()
        unit_group: str = get_unit_group()
        from_unit, to_unit = get_converter_unit(unit_group)
        new_value: float = converter(amount, unit_group, from_unit, to_unit)
    except (ValueError, KeyError, ZeroDivisionError) as e:
        sys.exit(str(e))

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
    return amount * (units[unit_group][from_unit]/units[unit_group][to_unit])
    

if __name__ == "__main__":
    main()