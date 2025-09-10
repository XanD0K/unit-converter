from unit_converter.data_manager import load_data

class UnitConverter:
    def __init__(self):
        self.units, self.base_units, self.conversion_log, self.unit_aliases, self.month_days = load_data()