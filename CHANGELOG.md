# Changelog

## [Unreleased]
### Added
- Added comman-line instructions

### Changed

### Fixed

### Removed




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
- Removed "actions" logic from `main`


## [0.2.0] - 2025-08-26
### Added
- Implemented `while` loops to keep user inside the program until he proactively quits
- Removed `sys.exit` to prevent abrupt exits from the program
- Implemented actions to allow user choose what to do

### Changed
- Removed multiple try-except blocks throughout the code, centralizing all in `main`
- Improved error checking for user's input


## [0.1.0] - 2025-08-26
### Added
- Implemented first functional structure for unit conversion