import json
import sys

from unit_converter.data_manager import load_data
from unit_converter.data_models import ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData
from unit_converter.utils import validate_unit_group
from project import print_groups, print_history, print_types, conversion_logic, manage_group, manage_type, manage_aliases, change_base_unit


class Converter:
    def __init__(self):
        try:
            # Initiates a 'DataStore' object
            self.units, self.base_units, self.conversion_log, self.unit_aliases, self.month_days = load_data()
            # Generates a global list containing all month's names
            self.all_months = [next(iter(value)) for value in self.month_days.values()]
        except (ValueError, FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error: {e}")
            raise

    def groups(self):
        print_groups(self)

    def history(self, limit=10):
        try:
            limit = int(limit)
            if limit < 0:
                raise ValueError("'limit' must be a positive number!")
        except (ValueError, TypeError):
            raise ValueError("'limit' must be a positive number!")
        print_history(self, limit)

    def types(self, unit_group):
        validate_unit_group(unit_group, self)
        print_types(self, unit_group.lower())

    def convert(self, unit_group, user_input):
        convert_data = ConversionData(
            unit_group = unit_group
        )
        if unit_group == "time":
            if not len(user_input.strip()) >= 2:
                raise ValueError("Incorrect format! Usage: <unit_group> <time_input>")
            convert_data.time_input = user_input.lower()
        else:
            args = user_input.split()
            if len(args) != 3:
                raise ValueError("Incorrect format! Usage: <unit_group> <from_type> <to_type> <amount>")
            convert_data.from_type, convert_data.to_type, convert_data.amount = args
            conversion_logic(self, convert_data)


    def manage_group(self, unit_group, user_input):
        args = user_input.split()
        if len(args) not in [1, 2]:
            raise ValueError("Incorrect format! Usage: <unit_group> <action> [new_base_unit]")
        action = args[0]
        new_base_unit = args[1] if len(args) == 2 else None
        manage_group_data = ManageGroupData(
            unit_group = unit_group.lower(),
            action = action.lower(),
            new_base_unit = new_base_unit.lower()
        )
        manage_group(self, manage_group_data)

    def manage_type(self, unit_group, user_input):
        validate_unit_group(unit_group.lower(), self)
        args = user_input.split()
        if len(args) not in [2, 3, 5]:
            raise ValueError("Incorrect format! Usage: <unit_group> <unit_type> <action> <value> [factor] [offset]")
        unit_type, action = args[:2]
        value = args[2] if len(args) >= 3 else None
        factor = args[3] if len(args) == 5 else None
        offset = args[4] if len(args) == 5 else None

        manage_type_data = ManageTypeData(
            unit_group = unit_group.lower(),
            unit_type = unit_type.lower(),
            action = action.lower(),
            value = value,
            factor = factor,
            offset = offset
        )
        manage_type(self, manage_type_data)

    def aliases(self, unit_group, user_input):
        validate_unit_group(unit_group.lower(), self)
        args = user_input.split()
        if len(args) != 3:
            raise ValueError("Incorrect format! Usage: <unit_group> <unit_type> <alias> <action>")
        unit_type, action, alias = args
        alias_data = AliasesData(
            unit_group = unit_group.lower(),
            unit_type = unit_type.lower(),
            action = action.lower(),
            alias = alias.lower()
        )
        manage_aliases(self, alias_data)

    def change_base(self, unit_group, user_input):
        validate_unit_group(unit_group.lower(), self)
        args = user_input.split()
        if len(args) != 1:
            raise ValueError("Incorrec format! Usage: <unit_group> <new_base_unit>")
        new_base_unit = args[0]
        change_base_data = ChangeBaseData(
            unit_group = unit_group.lower(),
            new_base_unit = new_base_unit.lower()
        )
        change_base_unit(self, change_base_data)