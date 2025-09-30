import json

from .data_manager import load_data
from .data_models import DataStore, ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData, validate_args_number
from .utils import validate_unit_group
from project import print_groups, print_history, print_types, conversion_logic, manage_group, manage_type, manage_aliases, change_base_unit


class Converter(DataStore):
    def __init__(self):
        try:
            # Initiates data variables related to all '.json' files
            units, base_units, conversion_log, unit_aliases, month_days, original_units, month_aliases = load_data()
            # Used to call the constructor from the parent class
            super().__init__(units, base_units,conversion_log,unit_aliases, month_days, original_units, month_aliases)
        except (ValueError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error: {str(e)}")
            raise
    
    # 'groups' action
    def groups(self) -> str:
        """Prints all unit groups"""
        message = print_groups(self)
        return message

    # 'history' action
    def history(self, limit: int=10, *args, **kwargs) -> str:
        """Prints the last conversion entries (default = 10)"""
        try:
            validate_args_number(*args, command="history", **kwargs)
            message = print_history(self, limit)
            return message
        except (ValueError, TypeError) as e:
            return f"Error: {str(e)}"

    # 'types' action
    def types(self, unit_group: str, *args, **kwargs) -> str:
        """Prints all unit types for a specific unit_group"""
        try:
            validate_args_number(*args, command="types", **kwargs)
            message = print_types(self, unit_group.lower())
            return message
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    # 'convert' action
    def convert(self, unit_group: str, user_input: str, *args, print_message: bool=False, **kwargs):
        """Handles all conversion logic"""
        try:
            validate_args_number(*args, command="convert", **kwargs)
            conversion_data = ConversionData(
                unit_group = unit_group.lower()
            )
            if unit_group == "time":
                conversion_data.time_input = user_input.lower()
            else:
                input_args = user_input.split()
                if len(input_args) != 3:
                    raise ValueError("Incorrect format! Usage: <unit_group> <from_type> <to_type> <amount>")
                conversion_data.from_type, conversion_data.to_type, conversion_data.amount = input_args
            message = conversion_logic(self, conversion_data)
            if print_message:
                return message
            return conversion_data.new_time if unit_group == "time" else conversion_data.new_value
        except (ValueError, KeyError, ZeroDivisionError, AttributeError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    # 'manage-group' action
    def manage_group(self, unit_group: str, user_input: str, *args, print_message: bool=False, **kwargs):
        """Allows to add/remove unit groups"""
        try:
            validate_args_number(*args, command="manage-group", **kwargs)
            user_args = user_input.split()
            if len(user_args) not in [1, 2]:
                raise ValueError("Incorrect format! Usage: <unit_group> <action> [new_base_unit]")
            action = user_args[0]
            new_base_unit = user_args[1] if len(user_args) == 2 else None
            manage_group_data = ManageGroupData(
                unit_group = unit_group.lower(),
                action = action.lower(),
                new_base_unit = new_base_unit.lower() if new_base_unit else None
            )
            return self._check_for_print(manage_group, manage_group_data, print_message)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    # 'manage-type' action
    def manage_type(self, unit_group: str, user_input: str, *args, print_message: bool=False, **kwargs):
        """Allows to add/remove unit types"""
        try:
            validate_args_number(*args, command="manage-type", **kwargs)
            validate_unit_group(unit_group.lower(), self)
            input_args = user_input.split()
            if len(input_args) not in [2, 3, 4]:
                raise ValueError("Incorrect format! Usage: <unit_group> <unit_type> <action> <value> [factor] [offset]")
            if len(input_args) == 4 and unit_group != "temperature":
                raise ValueError("Incorrect format! Usage: <unit_group> <unit_type> <action> <value> [factor] [offset]")

            action, unit_type = input_args[:2]
            value = input_args[2] if len(input_args) >= 3 else None
            factor = input_args[2] if len(input_args) >= 3 else None
            offset = input_args[3] if len(input_args) == 4 else None

            manage_type_data = ManageTypeData(
                unit_group = unit_group.lower(),
                action = action.lower(),
                unit_type = unit_type.lower(),
                value = value,
                factor = factor,
                offset = offset
            )
            return self._check_for_print(manage_type, manage_type_data, print_message)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    # 'aliases' action
    def aliases(self, unit_group: str, user_input: str, *args, print_message: bool=False, **kwargs):
        """Allows to add/remove aliases for a unit type"""
        try:
            validate_args_number(*args, command="aliases", **kwargs)
            validate_unit_group(unit_group.lower(), self)
            input_args = user_input.split()
            if len(input_args) != 3:
                raise ValueError("Incorrect format! Usage: <unit_group> <unit_type> <alias> <action>")
            action, unit_type, alias = input_args
            aliases_data = AliasesData(
                unit_group = unit_group.lower(),
                unit_type = unit_type.lower(),
                action = action.lower(),
                alias = alias.lower()
            )
            return self._check_for_print(manage_aliases, aliases_data, print_message)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    # 'change-base' action
    def change_base(self, unit_group: str, user_input: str, *args, print_message: bool=False, **kwargs):
        """Allows to change base unit for a specific unit_group"""
        try:
            validate_args_number(*args, command="change-base", **kwargs)
            validate_unit_group(unit_group.lower(), self)
            if len(user_input.split()) != 1:
                raise ValueError("Incorrec format! Usage: <unit_group> <new_base_unit>")
            new_base_unit = user_input.split()[0]
            change_base_data = ChangeBaseData(
                unit_group = unit_group.lower(),
                new_base_unit = new_base_unit.lower()
            )
            return self._check_for_print(change_base_unit, change_base_data, print_message)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {e.args[0] if e.args else str(e)}"

    def _check_for_print(self, function, data, print_message: bool=False):
        """Checks if user wants to print the output message"""
        message = function(self, data)
        if print_message:
            print(message)
        return message

    # Class methods aliases
    g = groups
    h = history
    t = types
    c = convert
    mg = manage_group
    mt = manage_type
    a = aliases
    cb = change_base