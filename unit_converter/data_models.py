from typing import Optional

from .utils import validate_unit_group, resolve_aliases, parse_time_input, parse_date_input, validate_date


class DataStore:
    """Holds data from all '.json' files"""
    def __init__(self, units: dict, base_units: dict, conversion_log: list, unit_aliases: dict, month_days: dict, original_units: dict):
        self.units = units
        self.base_units = base_units
        self.conversion_log = conversion_log
        self.unit_aliases = unit_aliases
        self.month_days = month_days
        self.original_units = original_units
        # Generates a global list containing all month's names
        self.all_months = [next(iter(value)) for value in month_days.values()]


class ConversionData:
    """Holds unit data related to unit conversion"""
    def __init__(self, unit_group: str, from_type: Optional[str]=None, to_type: Optional[str]=None, amount: Optional[str]=None, new_value: Optional[str]=None, time_input: Optional[str]=None, from_time: Optional[str]=None, to_time: Optional[str]=None, factor_time: Optional[str]=None, new_time: Optional[str]=None):
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

    def validate_from_type(self, data: DataStore) -> None:
        if(resolve_aliases(data, self.unit_group, self.from_type)):
            self.from_type = resolve_aliases(data, self.unit_group, self.from_type)
        if not self.from_type:
            raise ValueError("'unit_type' cannot be empty!")
        if self.from_type not in data.units[self.unit_group]:
            raise KeyError("Invalid unit type!")

    def validate_to_type(self, data: DataStore) -> None:
        if(resolve_aliases(data, self.unit_group, self.to_type)):
            self.to_type = resolve_aliases(data, self.unit_group, self.to_type)
        if not self.to_type:
            raise ValueError("'unit_type' cannot be empty!")
        if self.to_type not in data.units[self.unit_group]:
            raise KeyError("Invalid unit type!")

    def validate_amount(self) -> None:
        if self.amount is None:
            raise ValueError("'amount' cannot be empty")
        # Ensures amount is a number
        try:
            self.amount = float(self.amount)
        except:
            raise ValueError("Invalid amount!")
        # Prevents negative value for "Kelvin"
        if self.amount < 0 and self.unit_group == "temperature" and self.from_type == "kelvin":
            raise ValueError("Kelvin temperature cannot be negative!")

    def validate_time_input(self) -> None:
        if not self.time_input:
            raise ValueError("Time conversion can't be empty! Enter an expression!")
        if not len(self.time_input.split()) >= 2:
                raise ValueError("Incorrect format for time conversion!")
           
    def validate_from_time(self, data: DataStore) -> None:
        if not self.from_time:
            raise ValueError("Enter a value to convert from!")
        elif resolve_aliases(data, self.unit_group, self.from_time) in data.units[self.unit_group]:
            self.from_time = resolve_aliases(data, self.unit_group, self.from_time)
        elif parse_time_input(self.from_time) is not None:
            pass
        elif self.from_time in data.all_months:
            pass
        elif parse_date_input(self.from_time) is not None:
            years, months, days = parse_date_input(self.from_time) 
            if self.to_time:
                validate_date(years, months, days)
        else:
            raise ValueError(f"Invalid 'from_time': '{self.from_time}'")

    def validate_to_time(self, data: DataStore) -> None:
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
            raise ValueError(f"Invalid 'to_time': '{self.to_time}'")

    def validate_factor_time(self, data: DataStore) -> None:
        if not self.factor_time:
            raise ValueError("'factor_time' cannot be empty!")
        try:
            self.factor_time = float(self.factor_time)
        except ValueError:
            factor_time = resolve_aliases(data, self.unit_group, self.factor_time)
            if factor_time  is False or factor_time not in data.units[self.unit_group]:
                raise KeyError(f"Factor time '{self.factor_time}' not found in '{self.unit_group}' group!")
            self.factor_time = factor_time

    def validate_time_args(self, data: DataStore) -> None:
        args: list[str] = self.time_input.split()
        if len(args) == 2:
            self.from_time, self.factor_time = args
            self.validate_from_time(data)
            self.validate_factor_time(data)
        elif len(args) == 3:
            self.from_time, self.to_time, self.factor_time = args
            self.validate_from_time(data)
            self.validate_to_time(data)
            self.validate_factor_time(data)
        elif len(args) % 2 != 0 and len(args) > 3:
            self.to_time = args[-1]
            self.validate_to_time(data)
            for number, unit in zip(args[0::2], args[1::2]):
                try:
                    float(number)
                except:
                    raise ValueError(f"'{number}' is an invalid amount!")
                if resolve_aliases(data, self.unit_group, unit):
                    unit: str = resolve_aliases(data, self.unit_group, unit)
                if unit is False or unit not in data.units[self.unit_group]:
                    raise ValueError(f"'{unit}' is not a type for '{self.unit_group}' group!")
        else:
            raise ValueError("Invalid format for date and time conversion!")

    def validate_for_conversion(self, data: DataStore) -> None:
        validate_unit_group(self.unit_group, data)
        if self.unit_group == "time":
            self.validate_time_input()
            self.validate_time_args(data)
        else:   
            if (self.from_type is None and self.to_type is None and self.amount is None):
                raise ValueError("Invalid conversion format!")
            self.validate_from_type(data)
            self.validate_to_type(data)
            self.validate_amount()


class ManageGroupData:
    """Holds unit data related to creation/deletion of unit groups"""
    def __init__(self, unit_group: str, action: Optional[str]=None, new_base_unit: Optional[str]=None):
        self.unit_group = unit_group
        self.action = action
        self.new_base_unit = new_base_unit

    def validate_action(self) -> None:
        if not self.action:
            raise ValueError("'action' cannot be empty!")
        if self.action not in ["add", "remove"]:
            raise ValueError(f"Invalid action: '{self.action}'")

    def validate_add_action(self, data: DataStore) -> None:
        if self.unit_group in data.units:
            raise KeyError(f"'{self.unit_group}' is already an existed group!")
           
    def validate_remove_action(self,data: DataStore) -> None:
        if self.unit_group not in data.units:
            raise KeyError(f"'{self.unit_group}' is not a valid group!")
        if self.new_base_unit:
            raise ValueError("Incorrect usage when removing a group! Usage: <unit_group> remove")
        
    def validate_new_base_unit(self, data: DataStore) -> None:
        if not self.new_base_unit:
            raise ValueError("'new_base_unit' cannot be empty")
        if self.new_base_unit in data.units:
            raise KeyError(f"'{self.new_base_unit}' is already an unit group name!")
        if self.new_base_unit == self.unit_group:
            raise ValueError(f"'new_base_unit' can't have the same name as 'unit_group'")

    def validate_for_manage_group(self, data: DataStore) -> None:
        self.validate_action()
        if self.action == "add":
            self.validate_add_action(data)
            self.validate_new_base_unit(data)
        elif self.action == "remove":
            validate_unit_group(self.unit_group, data)
            self.validate_remove_action(data)


class ManageTypeData:
    """Holds unit data related to creation/deletion of unit types"""
    def __init__(self, unit_group: str, unit_type: Optional[str]=None, action: Optional[str]=None, value: Optional[str]=None, factor: Optional[str]=None, offset: Optional[str]=None):
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.action = action
        self.value = value
        self.factor = factor
        self.offset = offset

    def validate_action(self) -> None:
        if not self.action:
            raise ValueError("'action' cannot be empty!")
        if self.action not in ["add", "remove"]:
            raise ValueError(f"Invalid action: '{self.action}'")

    def validate_add_action(self, data: DataStore) -> None:        
        if not self.unit_type:
            raise ValueError("You can't leave that field empty!")
        if self.unit_type in data.units:
            raise KeyError(f"'{self.unit_type}' is already an unit group name!")
        elif self.unit_type in data.units[self.unit_group]:
            raise ValueError(f"'{self.unit_type}' is already an unit type in '{self.unit_group}' group!")
        elif self.unit_type in data.unit_aliases[self.unit_group]: 
            raise ValueError(f"'{self.unit_type}' is already being used as an alias in '{self.unit_group}' group")

    def validate_remove_action(self, data: DataStore) -> None:
        if resolve_aliases(data, self.unit_group, self.unit_type):
            self.unit_type = resolve_aliases(data, self.unit_group, self.unit_type)
        if not self.unit_type:
            raise ValueError("You can't leave that field empty!")
        elif self.unit_type not in data.units[self.unit_group]:
            raise ValueError(f"'{self.unit_type}' is not an unit type in '{self.unit_group}' group!")
        elif self.unit_type == data.base_units[self.unit_group]:
            raise ValueError("Cannot remove base unit!")
        if self.value or self.factor or self.offset:
            raise ValueError("Incorrect usage when removing a type! Usage: <unit_group> remove <unit_type>")

    def validate_value(self) -> None:
        if not self.value:
            raise ValueError("'value' cannot be empty!")
        try:
            self.value = float(self.value)
        except:
            raise ValueError("Invalid conversion factor!")

    def validate_factor(self) -> None:
        if not self.factor:
            raise ValueError("'factor' cannot be empty!")
        try:
            self.factor = float(self.factor)
        except:
            raise ValueError("Invalid conversion factor!")
        if self.factor <= 0:
            raise ValueError("Conversion factor must be positive!")

    def validate_offset(self) -> None:
        if not self.offset:
            raise ValueError("'offset' cannot be empty!")
        try:
            self.offset = float(self.offset)
        except:
            raise ValueError("Invalid conversion offset!")

    def validate_for_manage_type(self, data: DataStore) -> None:
        validate_unit_group(self.unit_group, data)
        self.validate_action()
        if self.action == "add":
            self.validate_add_action(data)            
            if self.unit_group == "temperature":
                self.validate_factor()
                self.validate_offset()
            else:
                self.validate_value()
        elif self.action == "remove":
            self.validate_remove_action(data)


class AliasesData:
    """Holds unit related data"""
    def __init__(self, unit_group: str, unit_type: Optional[str]=None, action: Optional[str]=None, alias: Optional[str]=None):
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.action = action
        self.alias = alias

    def validate_unit_type(self, data: DataStore) -> None:
        if self.unit_type not in data.units[self.unit_group]:
            raise KeyError(f"'{self.unit_type}' is not a valid unit type for '{self.unit_group}' group!")

    def validate_action(self) -> None:
        if not self.action:
            raise ValueError("'action' cannot be empty!")
        if self.action not in ["add", "remove"]:
            raise ValueError(f"Invalid action: '{self.action}'")

    def validate_alias(self, data: DataStore) -> None:
        if not self.alias:
            raise ValueError("'alias' cannot be empty!")
        all_group_aliases: list[str] = [alias for alias in data.unit_aliases[self.unit_group]]
        if self.action == "add":
            if self.alias in all_group_aliases:
                raise ValueError(f"'{self.alias}' is already being used as an alias in '{self.unit_group}'!")
            if self.alias in data.base_units:
                raise KeyError(f"'{self.alias}' is already being used to name an unit group!")
            if self.alias in data.units[self.unit_group]:
                raise KeyError(f"'{self.alias}' is already being used as an unit type in '{self.unit_group}' group!")
        elif self.action == "remove":
            if self.alias not in all_group_aliases:
                raise ValueError(f"'{self.alias}' is not an alias of '{self.unit_group}' group")
            if data.unit_aliases[self.unit_group][self.alias] != self.unit_type:
                raise ValueError(f"'{self.alias}' is not an alias for '{self.unit_type}'")

    def validate_for_aliases(self, data: DataStore) -> None:
        validate_unit_group(self.unit_group, data)
        if resolve_aliases(data, self.unit_group, self.unit_type):
            self.unit_type = resolve_aliases(data, self.unit_group, self.unit_type)
        self.validate_unit_type(data)
        self.validate_action()
        self.validate_alias(data)


class ChangeBaseData:
    """Holds unit data related to changing base unit"""
    def __init__(self, unit_group: str, new_base_unit: Optional[str]=None):
        self.unit_group = unit_group
        self.new_base_unit = new_base_unit

    def validate_for_change_base(self, data: DataStore) -> None:
        validate_unit_group(self.unit_group, data)
        if resolve_aliases(data, self.unit_group, self.new_base_unit):
            self.new_base_unit = resolve_aliases(data, self.unit_group, self.new_base_unit)        
        if not self.new_base_unit:
            raise ValueError("Unit type cannot be empty!")
        elif self.new_base_unit not in data.units[self.unit_group] or self.new_base_unit is False:
            raise KeyError(f"'{self.new_base_unit}' is not an unit type for '{self.unit_group}' group")
        elif self.new_base_unit == data.base_units[self.unit_group]:
            raise ValueError(f"'{self.new_base_unit}' is already the current base unit for '{self.unit_group}' group")   


def validate_for_history(data: DataStore, limit):
    """Validate 'conversion_log.json' data, and 'limit' value"""
    if not data.conversion_log:
        raise ValueError("Conversion history is empty!")
    try:
        limit = int(limit)
    except:
        raise ValueError("'limit' must be a number!")
    if int(limit) < 0:
        raise ValueError("'limit' must be a positive number!")


def validate_args_number(*args, command: str, **kwargs) -> None:
    if args:
        raise TypeError(f"Too many positional arguments for '{command}' command!")
    if kwargs:
        raise TypeError(f"Unexpected keyword argument for '{command}' command!")