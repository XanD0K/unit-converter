from utils import resolve_aliases, parse_time_input, parse_date_input, validate_date


class ConversionData:
    """Holds data from all '.json' files"""
    def __init__(self, units, base_units, conversion_log, unit_aliases, month_days):
        self.units = units
        self.base_units = base_units
        self.conversion_log = conversion_log
        self.unit_aliases = unit_aliases
        self.month_days = month_days
        # Generates a global list containing all month's names
        self.all_months = [next(iter(value)) for value in month_days.values()]


class UnitData:
    """Holds unit related data"""
    def __init__(self, unit_group, from_type=None, to_type=None, amount=None, new_value=None, time_input=None, from_time=None, to_time=None, factor_time=None, new_time=None, action=None, value=None, alias=None, factor=None, offset=None):
        self.unit_group = unit_group
        self.from_type = from_type
        self.to_type = to_type
        self.amount = amount
        self.new_value = new_value
        self.time_input = time_input
        self.from_time = from_time
        self.to_time = to_time
        self.factor_time = factor_time
        self.new_time = new_time
        self.action = action
        self.value = value
        self.alias = alias
        self.temp_factor = factor
        self.temp_offset = offset


    @staticmethod
    def validate_unit_group(unit_group, data, name=None):
        if not unit_group:
            raise ValueError("Unit group cannot be empty!")
        if name != "manage_type":
            if unit_group not in data.units:
                raise KeyError(f"{unit_group} is not a valid group!")

    def validate_from_type(self, data):
        if not self.from_type:
            raise ValueError("Unit type cannot be empty!")
        if self.from_type not in data.units[self.unit_group]:
            raise KeyError("Invalid unit type!")

    def validate_to_type(self, data):
        if not self.to_type:
            raise ValueError("Unit type cannot be empty!")
        if self.to_type not in data.units[self.unit_group]:
            raise KeyError("Invalid unit type!")

    def validate_amount(self):
        if not self.amount:
            raise ValueError("Amount cannot be empty")
        # Ensures amount is a number
        try:
            self.amount = float(self.amount)
        except:
            raise ValueError("Invalid amount!")
        # Prevents negative value for "Kelvin"
        if self.amount < 0 and self.from_type == "kelvin":
            raise ValueError("Kelvin temperature cannot be negative!")
        
    def validate_time_input(self):
        if not self.time_input:
            raise ValueError("Time conversion can't be empty! Enter an expression!")

    def validate_from_time(self, data):
        if not self.from_time:
            ValueError("Enter a value to convert from!")
        elif resolve_aliases(data, self.unit_group, self.from_time) in data.units[self.unit_group]:
            self.from_time = resolve_aliases(data, self.unit_group, self.from_time)
        elif parse_time_input(self.from_time) is not None:
            pass
        elif self.from_time in data.all_months:
            pass
        elif parse_date_input(self.from_time) is not None:
            years, months, days = parse_date_input(self.from_time)
            validate_date(years, months, days)  
        else:
            raise ValueError(f"Invalid 'from_time': {self.from_time}")

    def validate_to_time(self, data):
        if not self.to_time:
            raise ValueError("Enter a value to convert to!")
        elif resolve_aliases(data, self.unit_group, self.to_time) in data.units[self.unit_group]:
            self.to_time = resolve_aliases(data, self.unit_group, self.to_time)
        elif parse_time_input(self.to_time) is not None:
            pass
        elif self.to_time in data.all_months:
            pass
        elif parse_date_input(self.to_time) is not None:
            years, months, days = parse_date_input(self.to_time)
            validate_date(years, months, days)  
        else:
            raise ValueError(f"Invalid 'to_time': {self.to_time}")

    def validate_factor_time(self, data):
        if not self.factor_time:
            raise ValueError("'factor_time' cannot be empty!")
        try:
            self.factor_time = float(self.factor_time)
        except ValueError:
            factor_time = resolve_aliases(data, self.unit_group, self.factor_time)
            if factor_time  is False or factor_time not in data.units[self.unit_group]:
                raise KeyError(f"Unit type '{self.factor_time}' not found in '{self.unit_group}' group!")
            self.factor_time = factor_time

    def validate_time_args(self, data):
        args = self.time_input.split()
        if len(args) == 2:
            self.from_time, self.factor_time = args
            self.validate_from_time(data)
            self.validate_factor_time(data)
        elif len(args) == 3:
            self.from_time, self.to_time, self.factor_time = args
            self.validate_from_time(data)
            self.validate_to_time(data)
            self.validate_factor_time(data)
        elif len(args) % 2 != 0 and len(args) > 2:
            self.to_time = args[-1]
            self.validate_to_time(data)
            for number, unit in zip(args[0::2], args[1::2]):
                try:
                    float(number)
                except:
                    raise ValueError(f"'{number}' is an invalid amount!") 
                unit = resolve_aliases(data, self.unit_group, unit)           
                if unit not in data.units[self.unit_group]:
                    raise ValueError(f"'{unit}' is not a type for '{self.unit_group}' group!")
        else:
            raise ValueError("Invalid format for date and time conversion!")

    def validate_for_conversion(self, data):
        self.validate_unit_group(self.unit_group, data)
        if self.unit_group == "time":
            self.validate_time_input()
            self.validate_time_args(data)
        else:
            if not(self.from_type and self.to_type and self.amount is not None):
                raise ValueError("Invalid conversion format!")
            self.validate_from_type(data)
            self.validate_to_type(data)
            self.validate_amount()