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