# TODO


## New features
- [ ] Add style to introductory messages and instruction messages and add separator (e.g. with `-`, `=` or `_`)
- [ ] Use `inflect` library to output singular/plural unit group/type
- [ ] Add `money` group to allow currency conversion through API requests

## Refactoring tasks
- [ ] Reestructure the code by adding a class that encapsulates all programs logic
- [ ] Add remmaining comments throughout the codebase
- [ ] Add remmaining type hints throughout the codebase
- [ ] Clean program by removing multiple repetitive logic throught the codebase and transforming it into a single function
- [ ] Reestructure `project.py` file into multiple files to keep program cleaner (after adding Class)
- [ ] Reestructure `final-project` directory
- [ ] Check and improve `converter_time` function


## Testing
- [ ] Implement a test suite (`test_project.py`)
- [ ] Validade type checking (by using `mypy`)


## BACKLOG
- [ ]


## DONE
- [x] Implement a functional `converter` function
- [x] Improve Errors checking
- [x] Centralize try-except block in `main`, making functions to just raise the exception
- [x] Keep user inside program with `while` loop, until he decides to quit
- [x] Allow users to modify the unit's dictionary by adding new groups/types (modifies `units.json` and `base_units.json`)
- [x] Move `units` dictionary to another file to keep `project.py` cleaner
- [x] Use `json` library to open/save/close that new dictionary file, so that changes won't be lost
- [x] Remove abrupt ending with `sys.exit` by adding `while` logic
- [x] Remove actions' logic from `main` to keep it cleaner
- [x] Fix message that outputs dictionary's keys
- [x] Create separate functions for each action
- [x] Modify "add" action by adding more logic and validation checks to new groups (e.g. base unit, valid number)
- [x] When adding new group/type, display base unit of that type so that user knows in ehich unit he should calculate the conversion factor
- [x] Add separate logic for temperature (for converting units and for adding new types)
- [x] Fix converted value that always has 5 decimal values, even if all zeroes
- [x] Improve inputs validation based on unit group
- [x] Validate dictionary after importing/using it
- [x] Verify both dictionaries matches
- [x] Allow users to run the program through command lines
- [x] Add `groups` and `types` functions to also be used with comman-line arguments
- [x] Implement comman-line arguments to "add" action
- [x] Add aliases to all command lines to improve UX (e.g "convert" and "c" will both be used to convert units)
- [x] Modify argument's name to keep consistency throughout the code
- [x] Add log file, keeping track of user's previous actions
- [x] Add temperature conversions to history log
- [x] Improve time conversion with `datetime` library
- [x] Allow time conversion between units (e.g. 5 hours to minutes) and between dates given a specified unit (e.g. 2023-12-17 2024-12-01 minutes)
- [x] Improve converted output
- [x] Changed `add_to_log` function to accept new logic for date time unit conversion
- [x] Changed `print_history` function also print new
- [x] Add new date and time conversion logic to be handled through command-line commands
- [x] Add aliases to unit types (e.g. "km" for "kilometer", "ft" for "feet", "min" for "minute")