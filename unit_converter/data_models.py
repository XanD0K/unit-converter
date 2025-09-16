from .utils import validate_unit_group, resolve_aliases, parse_time_input, parse_date_input, validate_date


class DataStore:
    """Holds data from all '.json' files"""
    def __init__(self, units, base_units, conversion_log, unit_aliases, month_days):
        self.units = units
        self.base_units = base_units
        self.conversion_log = conversion_log
        self.unit_aliases = unit_aliases
        self.month_days = month_days
        # Generates a global list containing all month's names
        self.all_months = [next(iter(value)) for value in month_days.values()]
        

class ConversionData:
    """Holds unit data related to unit conversion"""
    def __init__(self, unit_group, from_type=None, to_type=None, amount=None, new_value=None, time_input=None, from_time=None, to_time=None, factor_time=None, new_time=None):
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
        if self.amount is None:
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
                if unit is False or unit not in data.units[self.unit_group]:
                    raise ValueError(f"'{unit}' is not a type for '{self.unit_group}' group!")
        else:
            raise ValueError("Invalid format for date and time conversion!")

    def validate_for_conversion(self, data):
        if self.unit_group == "time":
            self.validate_time_input()
            self.validate_time_args(data)
        else:
            if not(self.from_type and self.to_type and self.amount is not None):
                raise ValueError("Invalid conversion format!")
            self.validate_from_type(data)
            self.validate_to_type(data)
            self.validate_amount()


class ManageGroupData:
    """Holds unit data related to creation/deletion of unit groups"""
    def __init__(self, unit_group, action=None, new_base_unit=None):
        self.unit_group = unit_group
        self.action = action
        self.new_base_unit = new_base_unit

    def validate_action(self):
        if not self.action:
            raise ValueError("'action' cannot be empty!")
        if self.action not in ["add", "remove"]:
            raise ValueError(f"Invalid action: '{self.action}'")

    def validate_add_action(self, data):
        if self.unit_group in data.units:
            raise KeyError(f"'{self.unit_group}' is already an existed group!")
           
    def validate_remove_action(self,data):
        if self.unit_group not in data.units:
            raise KeyError(f"'{self.unit_group}' is not a valid group!")

    def validate_for_manage_group(self, data):
        validate_unit_group(self.unit_group, data)
        self.validate_action()
        if self.action == "add":
            self.validate_add_action(data)
            # Validates new_base_unit
        elif self.action == "remove":
            self.validate_remove_action(data)


class ManageTypeData:
    """Holds unit data related to creation/deletion of unit types"""
    def __init__(self, unit_group, unit_type=None, action=None, value=None, factor=None, offset=None):
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.action = action
        self.value = value
        self.factor = factor
        self.offset = offset

    def validate_action(self):
        if not self.action:
            raise ValueError("'action' cannot be empty!")
        if self.action not in ["add", "remove"]:
            raise ValueError(f"Invalid action: '{self.action}'")

    def validate_add_action(self, data):
        if not self.unit_type:
            raise ValueError("You can't leave that field empty!")
        if self.unit_type in data.units:
            raise KeyError(f"'{self.unit_type}' is already an unit group name!")
        elif self.unit_type in data.units[self.unit_group]:
            raise ValueError(f"'{self.unit_type}' is already an unit type!")
        elif self.unit_type in data.unit_aliases[self.unit_group]: 
            raise ValueError(f"'{self.unit_type}' is already being used as an alias in '{self.unit_group}' group")

    def validate_remove_action(self, data):
        if not self.unit_type:
            raise ValueError("You can't leave that field empty!")
        elif self.unit_type not in data.units[self.unit_group]:
            raise ValueError(f"'{self.unit_type}' is not an unit type in '{self.unit_group}' group!")
        elif self.unit_type == data.base_units[self.unit_group]:
            raise ValueError("Cannot remove base unit!")

    def validate_value(self):
        if self.value is None:
            raise ValueError("'value' cannot be empty!")
        try:
            self.value = float(self.value)
        except:
            raise ValueError("Invalid conversion factor!")

    def validate_factor(self):
        if self.factor is None:
            raise ValueError("You can't leave a field empty!")
        try:
            self.factor = float(self.factor)
        except:
            raise ValueError("Invalid conversion factor or offset!")
        if self.factor <= 0:
            raise ValueError("Conversion factor must be positive!")

    def validate_offset(self):
        if self.offset is None:
            raise ValueError("You can't leave a field empty!")
        try:
            self.offset = float(self.offset)
        except:
            raise ValueError("Invalid conversion factor or offset!")

    def validate_for_manage_type(self, data):
        validate_unit_group(self.unit_group, data)
        if self.unit_group not in data.units:
            raise KeyError(f"'{self.unit_group}' is not a valid group!")
        self.validate_action()
        if self.action == "add":
            self.validate_add_action(data)
            self.validate_value()
            if self.unit_group == "temperature":
                self.validate_factor()
                self.validate_offset()
        elif self.action == "remove":
            self.validate_remove_action(data)


class AliasesData:
    """Holds unit related data"""
    def __init__(self, unit_group, unit_type=None, action=None, alias=None):
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.action = action
        self.alias = alias

    def validate_unit_type(self, data):
        if self.unit_type not in data.units[self.unit_group]:
            raise KeyError(f"'{self.unit_type}' is not a valid unit type for '{self.unit_group}' group!")

    def validate_alias(self, data):
        if not self.alias:
            raise ValueError("Alias cannot be empty!")
        all_group_aliases = [alias for alias in data.unit_aliases[self.unit_group]]
        if self.action == "add":
            if self.alias in all_group_aliases:
                raise ValueError(f"'{self.alias}' is already being used in {self.unit_group}!")
            if self.alias in data.base_units:
                raise KeyError(f"'{self.alias}' is already being used to name an unit group!")
            if self.alias in data.units[self.unit_group]:
                raise KeyError(f"'{self.alias}' is already being used as an unit type in '{self.unit_group}'!")

        elif self.action == "remove":
            if self.alias not in all_group_aliases:
                raise ValueError(f"'{self.alias}' is not an alias of '{self.unit_type}'")
            if data.unit_aliases[self.unit_group][self.alias] != self.unit_type:
                raise ValueError(f"'{self.alias}' is not an alias for '{self.unit_type}'")

    def validate_for_aliases(self, data):
        self.validate_unit_type(data)
        self.validate_alias(data)


class ChangeBaseData:
    """Holds unit data related to changing base unit"""
    def __init__(self, unit_group, new_base_unit=None):
        self.unit_group = unit_group
        self.new_base_unit = new_base_unit

    def validate_for_change_base(self, data):
        if not self.new_base_unit:
            raise ValueError("Unit type cannot be empty!")    
        elif self.new_base_unit not in data.units[self.unit_group]:
            raise KeyError(f"'{self.new_base_unit}' is not an unit type for '{self.unit_group}' group")
        elif self.new_base_unit == data.base_units[self.unit_group]:
            raise ValueError(f"'{self.new_base_unit}' is already the current base unit for '{self.unit_group}' group")