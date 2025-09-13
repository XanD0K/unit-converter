import calendar
import re

def validate_unit_group(unit_group, data, name=None):
    if not unit_group:
        raise ValueError("Unit group cannot be empty!")
    if name != "manage_type":
        if unit_group not in data.units:
            raise KeyError(f"'{unit_group}' is not a valid group!")

def get_converter_units(data, unit_data) -> tuple[str, str]:
    """Gets types of units"""
    unit_data.from_type = resolve_aliases(data, unit_data.unit_group, input("From: ").strip().lower())
    unit_data.validate_from_type(data)
    unit_data.to_type = resolve_aliases(data, unit_data.unit_group, input("To: ").strip().lower())
    unit_data.validate_to_type(data)
    return unit_data.from_type, unit_data.to_type


def get_amount(unit_data) -> float:
    """Gets unit amount"""
    unit_data.amount = input("Amount: ").strip()
    if not re.search(r"^-?\d+(\.\d+)?$", unit_data.amount):
        raise ValueError("Invalid amount! Please, insert integer or decimals! (e.g. 10 or 10.0)")        
    unit_data.validate_amount()
    return float(unit_data.amount)


def resolve_aliases(data, unit_group, unit_type):
    """Checks user's input for any match with unit type or unit's aliases"""
    # Checks for literal name
    if unit_type in data.units[unit_group]:
        return unit_type
    # Checks for aliases
    elif unit_type in data.unit_aliases[unit_group]:
        return data.unit_aliases[unit_group][unit_type]
    else:
        return False


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
    """Helper function for 'parse_time_input' function"""
    if time_str is not None:
        return int(time_str)
    else:
        return 0


def get_seconds(data, unit_group, years, months, days):
    """Returns the approximated duration of a data in seconds"""
    approx_year_duration = 365.2425 * data.units[unit_group]["days"]
    approx_month_duration = 30.436875 * data.units[unit_group]["days"]
    return years * approx_year_duration + months * approx_month_duration + days * data.units[unit_group]["days"]


def parse_date_input(time_str):
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


def calculate_leap_years(from_years, from_months, to_years, to_months, to_days):
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
    """Checks if a years is a leap year"""
    if (time_int % 4 == 0 and time_int % 100 != 0) or (time_int % 400 == 0):
        return True
    return False


def validate_date(year, month, day):
    """Prevents invalid date"""
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid date! '{month}' is not a valid month")
    max_days = calendar.monthrange(year, month)[1]
    if not 1 <= day <= max_days:
         raise ValueError(f"Invalid date! '{day}' is not a valid day for '{month}'")
    return True


def get_days_from_month(data, month):
    """Gets days for a specificed month's name"""
    return next((value[month] for value in data.month_days.values() if month in value), None)
    # return next((days for value in month_days.values() for name, days in value.items() if name==month), None)


def get_index_from_month(data, month):
    """Gets month's index given its name"""
    return next((int(index) for index, value in data.month_days.items() if month in value), None)


def gets_days_from_index(data, month_index):
    """Gets days for a specificed month's index"""
    return next(iter(data.month_days[month_index].values()), None)