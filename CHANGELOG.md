# Changelog

## [Unrelease]
### Added

### Changed

### Fixed


## [0.5.1] - 2025-08-29
### Added
- Added validation on user's input for Kelvin temperature
- Alert users for negative values!


## [0.5.0] - 2025-08-29
### Changed
- Changed conversion logic to first get user's input about unit group and then the amount to be converted. It allowed making input validations for a few units type (e.g. Kelvin)

### Fixed
- Fixed typos
- Fixed variables names `from_unit` and `to_unit` to be `from_type` and `to_type` respectively, to better describe that variable


## [0.4.0] - 2025-08-28
### Added
- Added logic for "temperature" group of units

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