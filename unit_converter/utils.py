import calendar
import re
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data_models import DataStore, ConversionData


def print_introductory_messages() -> None:
    """Prints introductory messages and instructions"""
    print("Welcome to unit converter!")
    print("To print conversion history, enter 'history'")
    print("To check all group of units available, enter 'groups'")
    print("To check all types for a specific group, enter 'types'")
    print("To convert an unit, enter 'convert'")
    print("To manage unit groups, enter 'manage-group'")
    print("To manage unit types, enter 'manage-types'")
    print("To manage aliases, enter 'aliases'")
    print("To change base unit for a group, enter 'change-base'")
    print("Quit anytime by entering 'quit' or by pressing ctrl+d or ctrl+c", end="\n\n")
    
    
def print_time_instructions() -> None:
    """Prints instructions for converting date and time units"""
    print("For date-time conversion, you can choose from different formats for conversion:")
    print(" - From a specific unit to another. Usage: <unit_type> <unit_type> [amount]")
    print(" - From a more complex time to another. Usage: HH:MM:SS HH:MM:SS <unit_type>")
    print(" - From one month to another. Usage: <month_name> <month_name> <unit_type>")
    print(" - From a date to another. Usage: YYYY-MM-DD YYYY-MM-DD <unit_type>")


def get_users_input(prompt: str) -> str:
    """
    Allows users to exit the program anytime by entering 'quit' on input
    It is used throughout codebase instead of 'input()'
    """
    value: str = input(prompt).strip().lower()
    if value == "quit":
        print("Bye!")
        sys.exit(0)
    return value


def get_unit_group(data: "DataStore") -> str:
    """Gets and validates unit group"""
    unit_group: str = get_users_input("Unit group: ").strip().lower()
    validate_unit_group(unit_group, data)
    return unit_group


def validate_unit_group(unit_group: str, data: "DataStore") -> None:
    if not unit_group:
        raise ValueError("Unit group cannot be empty!")
    if unit_group not in data.units:
        raise KeyError(f"'{unit_group}' is not a valid group!")


def get_converter_units(data: "DataStore", unit_data: "ConversionData") -> tuple[str, str]:
    """Gets unit_type for conversion"""
    unit_data.from_type = resolve_aliases(data, unit_data.unit_group, get_users_input("From: ").strip().lower())
    unit_data.validate_from_type(data)
    unit_data.to_type = resolve_aliases(data, unit_data.unit_group, get_users_input("To: ").strip().lower())
    unit_data.validate_to_type(data)
    return unit_data.from_type, unit_data.to_type


def get_amount(unit_data: "ConversionData") -> float:
    """Gets unit amount"""
    unit_data.amount = get_users_input("Amount: ").strip()
    if not re.search(r"^-?\d+(\.\d+)?$", unit_data.amount):
        raise ValueError("Invalid amount! Please, insert integer or decimals! (e.g. 10 or 10.0)")        
    unit_data.validate_amount()
    return float(unit_data.amount)


def resolve_aliases(data: "DataStore", unit_group: str, unit_type: str) -> str | None:
    """Checks user's input for any match with unit type or unit's aliases"""
    # Checks for literal name
    if unit_type in data.units[unit_group]:
        return unit_type
    # Checks for aliases
    elif unit_type in data.unit_aliases[unit_group]:
        return data.unit_aliases[unit_group][unit_type]
    else:
        return False


def parse_time_input(time_str: str) -> int | None:
    """Gets user's input of a time and outputs that correspondent value in seconds"""
    if matches := re.search(r"^(?:(\d+)h:)?(?:(\d+)m:)?(?:(\d+)s)?$", time_str):
        hours, minutes, seconds = matches.group(1), matches.group(2), matches.group(3)
        hours = check_time_is_none(hours)
        minutes = check_time_is_none(minutes)
        seconds = check_time_is_none(seconds)
        return hours * 3600 + minutes * 60 + seconds
    return None


def check_time_is_none(time_str: str) -> int:
    """Checks if a specific time unit was provided"""
    if time_str is None or time_str == '':
        return 0
    else:
        return int(time_str)


def get_seconds(data: "DataStore", unit_group: str, years: int, months: int, days: int) -> float:
    """Returns the approximated duration of a data in seconds"""
    try:
        approx_year_duration: float = 365.2425 * data.units[unit_group]["days"]
        approx_month_duration: float = 30.436875 * data.units[unit_group]["days"]
        return years * approx_year_duration + months * approx_month_duration + days * data.units[unit_group]["days"]
    except KeyError:
         raise KeyError(f"'{unit_group}' is not a valid group!")


def parse_date_input(time_str: str) -> tuple[int, int,int] | None:
    """Gets user's input of a date, and outputs the year, month and day"""
    if matches := re.search(r"^(\d+)-(\d+)-(\d+)$", time_str):
        year, month, day = map(int, matches.groups())
        return year, month, day
    return None


def format_value(value: float) -> str:
    """Format converted value by allowing only 5 decimal values and elimitating all trailling zeroes"""
    formatted_value = f"{value:,.5f}".rstrip("0").rstrip(".")
    # Adds '.0' if formatted value ended up with no decimal values
    if "." not in formatted_value:
        formatted_value += ".0"
    return formatted_value


def calculate_leap_years(from_years: int, from_months: int, to_years: int, to_months: int, to_days: int) -> int:
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


def is_leap(time_int: int) -> bool:
    """Checks if a years is a leap year"""
    if (time_int % 4 == 0 and time_int % 100 != 0) or (time_int % 400 == 0):
        return True
    return False


def validate_date(year: int, month: int, day: int) -> bool:
    """Prevents invalid date"""
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid date! '{month}' is not a valid month")
    max_days = calendar.monthrange(year, month)[1]
    if not 1 <= day <= max_days:
         raise ValueError(f"Invalid date! '{day}' is not a valid day for '{month}' month")
    return True


def get_days_from_month(data: "DataStore", month: str) -> int | None:
    """Gets days for a specificed month's name"""
    return next((value[month] for value in data.month_days.values() if month in value), None)
    # return next((days for value in month_days.values() for name, days in value.items() if name==month), None)


def get_index_from_month(data: "DataStore", month: str) -> int | None:
    """Gets month's index given its name"""
    return next((int(index) for index, value in data.month_days.items() if month in value), None)


def gets_days_from_index(data: "DataStore", month_index: str) -> int | None:
    """Gets days for a specificed month's index"""
    return next(iter(data.month_days[month_index].values()), None)