# Nested dictionaries that defines all units available
# Using SI(Internation System of Units) as base to this program
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
        "nautical mile": 1852.001,
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
        "US ton": 907.1847,
        "pound": 0.4535924,
        "ounce": 0.02834952,
    },

    "temperature": {
        "celcius": 1.0,  # Base unit
        "kelvin": -272.15,
        "fahrenheit": -17.22222
    },

    "volume": {
        "liter": 1.0,  # Base unit
        "milliliter": 0.001,
        "cup": 0.2365875,
        "teaspoon": 0.004928906,
        "gallon": 3.7854,        
        "cubic centimeter": 0.001,
        "cubic meter": 1000,
    },  

    "area": {
        "square meter": 1.0,  # Base unit
        "square centimeter": 0.0001,
        "square millimeter": 0.000001,
        "square inch": 0.00064516,
        "square feet": 0.09290304,
        "square mile": 2589988,
        "acre": 4046.86,
        "hectare": 10000,
        "are": 100,
    },

    "speed": {
        "kilometer per hour": 1.0,  # Base unit
        "meters per second": 3.6,
        "kilometers per second": 3600,
        "miles per hour": 1.609344,
        "foot per second": 1.09728,
        "knot": 1.852001,
        "sound": 1234.8,
    },
}


def main():
    value = int(input("Ammount: ").strip())
    unit_type = input("Unit type: ").strip().lower()
    from_unit = input("From: ").strip().lower()
    to_unit = input("To: ").strip().lower()

    print(f"{value} {from_unit} = {units[unit_type][from_unit] / units[unit_type][to_unit]} {to_unit}")



if __name__ == "__main__":
    main()