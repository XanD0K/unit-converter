import re
import sys

units = {
    "length": {
        "meter": 1.0,  # Base unit
        "centimeter": 0.01,
        "millimeter": 0.001,
        "kilometer": 1000.0,
        "feet": 0.3048,
        "inches": 0.0254,
        "yard": 0.9144,
        "mile": 1609.344,
        "nautical_mile": 1852.001,
    },

    "time": {
        "second": 1.0,  # Base unit
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400,
    },

    "mass": {
        "kilogram": 1.0,  # Base unit
        "gram": 0.001,
        "milligram": 0.000001,
        "tonne": 1000,
        "us_ton": 907.1847,
        "pound": 0.4535924,
        "ounce": 0.02834952,
    },

    "temperature": {
        "celsius": 1.0,  # Base unit
        "kelvin": -272.15,
        "fahrenheit": -17.22222
    },

    "volume": {
        "liter": 1.0,  # Base unit
        "milliliter": 0.001,
        "cup": 0.2365875,
        "teaspoon": 0.004928906,
        "gallon": 3.7854,        
        "cubic_centimeter": 0.001,
        "cubic_meter": 1000,
    },  

    "area": {
        "square_meter": 1.0,  # Base unit
        "square_centimeter": 0.0001,
        "square_millimeter": 0.000001,
        "square_inch": 0.00064516,
        "square_feet": 0.09290304,
        "square_mile": 2589988,
        "acre": 4046.86,
        "hectare": 10000,
        "are": 100,
    },

    "speed": {
        "km/h": 1.0,  # Base unit
        "m/s": 3.6,
        "km/s": 3600,
        "mph": 1.609344,
        "ft/s": 1.09728,
        "knot": 1.852001,
        "mach": 1234.8,
    },
}


def main():
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
    unit_type: str = input("Unit group: ").strip().lower()
    if not unit_type:
        raise ValueError("Unit group cannot be empty!")
    if unit_type not in units:
        raise KeyError("Invalid unit group!")
    return unit_type


def get_converter_unit(unit_type) -> tuple[str, str]:
    """Gets types of units user is convertind from and to"""
    from_unit: str = input("From: ").strip().lower()
    to_unit: str = input("To: ").strip().lower()
    if not from_unit or not to_unit:
        raise ValueError("Unit type cannot be empty!")
    if from_unit not in units[unit_type] or to_unit not in units[unit_type]:
        raise KeyError("Invalid unit type!")
    return from_unit, to_unit


def converter(amount, unit_type, from_unit, to_unit) -> float:
    """Convert one value to another"""
    return amount * (units[unit_type][from_unit]/units[unit_type][to_unit])
    

if __name__ == "__main__":
    main()