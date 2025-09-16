import json
import sys

from unit_converter.data_manager import load_data
from unit_converter.data_models import ConversionData, ManageGroupData, ManageTypeData, AliasesData, ChangeBaseData
from project import print_groups, print_history, print_types, manage_group, manage_type, manage_aliases, change_base_unit


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
        print_history(self, limit)

    def types(self, unit_group):
        print_types(self, unit_group)

    def convert(self):
        ...

    def manage_group(self, unit_group, action, new_base_unit=None):
        manage_group_data = ManageGroupData(
            unit_group = unit_group,
            action = action,
            new_base_unit = new_base_unit
        )
        manage_group(self, manage_group_data)

    def manage_type(self, unit_group, unit_type, action, value=None, factor=None, offset=None):
        manage_type_data = ManageTypeData(
            unit_group = unit_group,
            unit_type = unit_type,
            action = action,
            value = value,
            factor = factor,
            offset = offset
        )
        manage_type(self, manage_type_data)

    def aliases(self, unit_group, unit_type, action, alias):
        alias_data = AliasesData(
            unit_group = unit_group,
            unit_type = unit_type,
            action = action,
            alias = alias
        )
        manage_aliases(self, alias_data)

    def change_base(self, unit_group, new_base_unit):
        change_base_data = ChangeBaseData(
            unit_group = unit_group,
            new_base_unit = new_base_unit
        )
        change_base_unit(self, change_base_data)