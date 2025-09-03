# Changelog

## [Unreleased]
### Added

### Changed

### Fixed

### Removed

## [0.8.0] - 2025-09-03
### Added
- Created the `unit_alises.json` file that contains all aliases for each unit type
- Created 
- Modifies codebase to allow users accessing and modifying that `unit_alises.json` file


## [0.7.2] - 2025-09-02
### Added
- Modified `handle_cli` function to add conversion log to `conversion_log.json` file

### Changed
- Changed `handle_cli` function to accept that new logic for date and time unit conversions through command lines


## [0.7.1] - 2025-09-01
### Changed
- Changed `format_value` function to apply `,` to every group of 3 digits
- Also applying `format_value` function to inputs and to `history` command
- Modified `add_to_log` function to add date and time unit conversions to `conversin_log.json` file
- Modified `print_history` function to handle time conversions on log history


## [0.7.0] - 2025-09-01
### Added
- Created `converter_time` function to handle all date and time unit conversions
- Created `days_to_month.json` file to be used on date and time conversions
- Used Python's `datetime` library to improve date and time conversions
- Used Python's `math` library to always get positive values from date and time unit conversions


## [0.6.4] - 2025-08-31
### Fixed
- Created `add_to_log` function to also be used with temperature conversions


## [0.6.3] - 2025-08-31
### Added
- Created `conversion_log.json` file to keep track of user's previous conversions
- Added `history` command and logic to fill the new `.json` file and to print 

### Changed
- Changed argument's name `group` to `unit_group`, to keep consistency throughout codebase

### Fixed
- Fixed command-line aliases to accept aliases


## [0.6.2] - 2025-08-30
### Added
- Added aliases to each command, improving UX
- Created a copy of all arguments, lowering some of them, improving UX


## [0.6.1] - 2025-08-30
### Added
- Added comman-line logic for add action

### Fixed
- Fixed convertion logic for "temperature" units (was missing a `return` statement)


## [0.6.0] - 2025-08-29
### Added
- Added first functional structure to handle comman-line arguments (missing logic for "add" action)

### Changed
- Moved "groups" action to `print_groups` function and "types" action to `print_types` function to also be used with command-line arguments
- Modified command-line logic to exit the program after output, preventing users to continue in the program


## [0.5.4] - 2025-08-29
### Added
- Validated dictionaries structure before running
- Ensure dictionaries keys match


## [0.5.3] - 2025-08-29
### Added
- Added validation on user's input for Kelvin temperature
- Alert users for negative values!

### Changed
- Improved users input validation based on unit group


## [0.5.2] - 2025-08-29
### Changed
- Changed conversion logic to first get user's input about unit group and unit type and then get the amount to be converted, which allows making input validations (e.g. for Kelvin units)

### Fixed
- Fixed variables names `from_unit` and `to_unit` to be `from_type` and `to_type` respectively, to better describe that variable


## [0.5.1] - 2025-08-28
### Fixed
- Fixed print message by removing trailling zeroes


## [0.5.0] - 2025-08-28
### Added
- Added `converter_temp` function to handle "temperature" units
- Added `add_temp_logic` function to handle adding new types for "temperature" group

## Changed
- Changed temperature group in `units.json` dictionary so that each type accepts a tuple of 2 float values, instead of just one value

## [0.4.0] - 2025-08-28
### Added
- Added validation logic when adding new group/type
- Created separate functions for "add" and "convert" actions

### Changed
- Moved introductory messages and instructions out of `main`


## [0.3.1] - 2025-08-27
### Added
- Added introductory messages and instructions when user enters the program


## [0.3.0] - 2025-08-27
### Changed
- Moved `units` dictionary to `units.json` file, modifying it with `json` library
- Moved "actions" logic from `main`


## [0.2.0] - 2025-08-26
### Added
- Implemented `while` loops to keep user inside the program until he proactively quits
- Implemented actions to allow user choose what to do

### Changed
- Removed multiple try-except blocks throughout the codebase, centralizing all in `main`
- Improved error checking for user's input

### Removed
- Removed `sys.exit` to prevent abrupt exits from the program


## [0.1.0] - 2025-08-26
### Added
- Implemented first functional structure for unit conversion