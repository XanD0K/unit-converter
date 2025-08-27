# TODO


## New features
- [ ] Allow users to run the program through command lines
- [ ] Add separate logic for temperature
- [ ] Add type hints throughout the codebase
- [ ] Fix converted value that always has 5 decimal values, even if all zeroes
- [ ] Fix message that outputs dictionary's keys
- [ ] Use `json` library to open/save/close that new dictionary file, so that changes won't be lost
- [ ] When adding new group/type, display base unit of that type so that user knows the conversion factor
- [ ] Modify "add" action adding more logic and validation checks to new groups (e.g. base unit, valid number)


## Refactoring tasks
- [ ] Create a class to group all related functionalities
- [ ] Remove abrupt ending with `sys.exit` by adding `while` logic
- [ ] Remove actions' logic from `main` to keep it cleaner


## Testing
- [ ] Implement a test suite (`test_project.py`)
- [ ] Validade type checking (by using `mypy`)
- [ ] Improve inputs validation based on unit group


## BACKLOG
- [ ]


## DONE
- [x] Implement a functional `converter` function
- [x] Improve Errors checking
- [x] Centralize try-except block in `main`, making functions to just raise the exception
- [x] Keep user inside program with `while` loop, until he decides to quit
- [x] Allow users to modify the unit's dictionary by adding new groups/types
- [x] Moves dictionary to another file to keep `project.py` cleaner

