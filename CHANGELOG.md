# Changelog


## [Unreleased]
### Added
- Created `api.py` file with an `UnitConverter` class, which allow users to access the program by declaring class objects

### Changed

### Fixed

### Removed

## [0.9.4] - 2025-09-13
### Added
- Added option to remove unit groups in `manage_group` function

### Changed
- Changes `manage_type` to be unit_type specific. Now it only handles adding/removing unit_type
- Renamed `add_new_group` to `manage_group`, which now als allows to remove unit groups
- Segregated `UnitData` class into `ConversionData`, `ManageTypeData`, `AliasesData` and `ChangeBaseData` classes


## [0.9.3] - 2025-09-12
### Changed
- Centralized variables' validation in `UnitData` class, which were priviously segregated throught codebase
- Modified `handle_cli` to accept all validations from `UnitData`


## [0.9.2] - 2025-09-11
### Added
- Created `UnitData` class to hold all data related to units, keeping code cleaner

### Changed
- Restructured all code, removing `unit_group`, `from_type`, `to_type`, `amount`, `new_value`, `time_input`, `from_time`, `to_time`, `factor_time`, `new_time`, `action, value`, `alias`, `factor` and `offset` variables, which are all unit related variables, incorporating all into `UnitData` class to reduce number of functions' arguments
- Changed `handle_cli` function to accept `UnitData` class, improving readability and reducing number of arguments


## [0.9.1] - 2025-09-10
### Added
- Created `ConversionData` data class to hold all data from `.json` files, as well as `ALL_MONTHS` variable, keeping code cleaner

### Changed
- Restructured all code, removing `units`, `base_units`, `conversion_log`, `unit_aliases` and `month_days` variables, changing them to be just a call to that new `ConversionData` object


## [0.9.0] - 2025-09-09
### Added
- Created `unit_converter` directory which will contain all new files generated from `project.py` segmentation
- Created `data_manager.py` file to hold all functions that open/modify/save `.json` files
- Created `utils.py` file to hold all helper functions

### Changed
- Moved all `.json` files to `data` directory
- Changed `validate_dictionaries` function's name to `validate_data`


## [0.8.3] - 2025-09-08
### Changed
- Created `zero_division_checker` function that checks if a number is zero, preventing divisions by zero, which removes repetitive code throught codebase
- Changed `handle_cli` function to be case insensitive for "convert" action
- Moved "import dictionaries" logic into `import_json` function


## [0.8.2] - 2025-09-07
### Added
- Created `ALL_MONTHS` global variable containing all months's names in `month_days.json` file
- Created `get_days_from_month`, `get_index_from_month` and `gets_days_from_index` helper functions to handle different queries in `month_days.json` file 
- Created `clean_history` function that deletes all entries older than 3 days from `conversion_log.json` file, preventing dealing with a big file

### Changed
- Merged `month_index_days.json` and `month_indexes.json` files into `month_days.json` file, changing it's structure to suport multiple queries


## [0.8.1] - 2025-09-06
### Changed
- Changed `converter_time` function to receive `*args` as arguments, allowing even more complex conversions
- Changed `handle_cli` function to also allow multiple arguments with `*args`
- Changed `print_history` function to also print new conversion formats for `time` unit group


## [0.8.0] - 2025-09-05
### Added
- Implemented `get_seconds` function to calculate seconds from a given date
- Implemented `calculate_leap_years` function to calculate the number of leap years from 2 given dates
- Implemented `validate_date` function to validate a given date
- Added `month_index_days.json` dictionary to be used in date-time conversions


## [0.7.1] - 2025-09-04
### Added
- Created `month_days` dictionary that relates a month with its respective number of days, to improve date and time conversions
- Changed `add_logic` function to `manage_type`, improving it to allow users to remove unit types
- Added `change_base_unit` which allow users to change base unit for an unit group

### Changed
- Removed inner `while` loops that kept users inside action's logic
- Improved `get_amount` function, making it cleaner
- Improved `add_new_group` function, making it cleaner
- Changed `add_temp_logic` function name to `add_temp_type`


## [0.7.0] - 2025-09-03
### Added
- Created the `unit_alises.json` file that contains all aliases for each unit type
- Created `resolve_aliases` function to handle unit types and unit's aliases throughout codebase
- Created `manage_aliases` function to allow users adding and removing aliases to/from `unit_alises.json` file
- Added logic to `handle_cli` function that allows users to manage aliases, by adding/removing them to/from an unit type
- Added backup logic if modifying `.json` files failes

### Changed
- Changed "types" action to act like all other functions, keep consistency throughout codebase

### Removed
- Removed alerts for negative numbers inputed by users


## [0.6.1] - 2025-09-02
### Added
- Modified `handle_cli` function to add conversion log to `conversion_log.json` file

### Changed
- Changed `handle_cli` function to accept that new logic for date and time unit conversions through command lines


## [0.6.0] - 2025-09-01
### Added
- Created `converter_time` function to handle all date and time unit conversions
- Created `days_to_month.json` file to be used on date and time conversions
- Used Python's `datetime` library to improve date and time conversions
- Used Python's `math` library to always get positive values from date and time unit conversions

### Changed
- Changed `format_value` function to apply `,` to every group of 3 digits
- Also applying `format_value` function to inputs and to `history` command
- Modified `add_to_log` function to add date and time unit conversions to `conversin_log.json` file
- Modified `print_history` function to handle time conversions on log history


## [0.5.0] - 2025-08-31
### Added
- Created `conversion_log.json` file to keep track of user's previous conversions
- Added `history` command and logic to fill the new `.json` file and to print 

### Changed
- Changed argument's name `group` to `unit_group`, to keep consistency throughout codebase

### Fixed
- Fixed command-line logic to accept aliases
- Created `add_to_log` function to also be used with temperature conversions


## [0.4.1] - 2025-08-30
### Added
- Added comman-line logic for "add" action
- Added aliases to each command, improving UX
- Created a copy of all arguments, malipulating them instead of dealing with original list

### Fixed
- Fixed convertion logic for "temperature" units (was missing a `return` statement)


## [0.4.0] - 2025-08-29
### Added
- Added validation on user's input for Kelvin temperature
- Created alert for negative values input
- Created `validate_dictionaries` function to validated dictionaries structure before running the program
- Added first functional structure to handle comman-line arguments (missing logic for "add" action)

### Changed
- Changed conversion logic to first get user's input about unit group and unit type and then get the amount to be converted, which allows making input validations (e.g. for Kelvin units)
- Improved users input validation based on unit group
- Moved "groups" action to `print_groups` function and "types" action to `print_types` function to also be used with command-line arguments
- Modified command-line logic to exit the program after output, preventing users to continue in the program

### Fixed
- Fixed variables names `from_unit` and `to_unit` to be `from_type` and `to_type` respectively, to better describe that variable


## [0.3.0] - 2025-08-28
### Added
- Added validation logic when adding new group/type
- Created separate functions for "add" and "convert" actions
- Added `converter_temp` function to handle "temperature" units
- Added `add_temp_logic` function to handle adding new types for "temperature" group

### Changed
- Moved introductory messages and instructions out of `main` function
- Changed temperature group in `units.json` dictionary so that each type accepts a tuple of 2 float values ("factor" and "offset"), instead of just one value

### Fixed
- Fixed print message by removing trailling zeroes


## [0.2.0] - 2025-08-27
### Added
- Added introductory messages and instructions when user enters the program
- Implemented `while` loops to keep user inside the program until he proactively quits
- Implemented actions to allow user choose what to do

### Changed
- Removed multiple try-except blocks throughout the codebase, centralizing all in `main`
- Improved error checking for user's input
- Moved `units` dictionary to `units.json` file, modifying it with `json` library
- Moved "actions" logic out of `main` function 

### Removed
- Removed `sys.exit` to prevent abrupt exits from the program


## [0.1.0] - 2025-08-26
### Added
- Implemented first functional structure for unit conversion