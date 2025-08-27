# TODO


## New features
- [ ] Allow users to modify the unit's dictionary by adding new groups/types
- [ ] Allow users to run the program through command lines
- [ ] Add separate logic for temperature
- [ ] Fix output message that always outputs 5 decimal values, even if all zeroes


## Refactoring tasks
- [ ] Create a class to group all related functionalities
- [ ] Moves dictionary to another file to keep `project.py` cleaner
- [ ] Remove abrupt ending with `sys.exit` by adding `while` logic
- [ ] Keep user inside program with `while` loop, until he decides to quit


## Testing
- [ ] Implement a test suite (`test_project.py`)
- [ ] Validade type checking (by using `mypy`)
- [ ] Improve inputs validation based on unit group


## BACKLOG
- [ ]


## DONE
- [x] Implement a functional converter() function
- [x] Improve Errors checking
- [x] Centralize try-except block in main, making functions to just raise the exception
- [x] Add type hints throughout the codebase

