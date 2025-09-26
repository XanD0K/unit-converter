# UnitConverter
#### Video Demo:  <URL HERE>


## Description
This program has the purpose of converting units from different groups: "length", "time", "mass", "temperature", "volume", "area" and "speed".
In addition to that, users can create and to remove groups and types of units, as well as aliases for any unit type.
Users also have the ability to change the base unit of any group, which changes the conversion factor of all unit types in that specific group.
Lastly, he can also access the history log, which contains all previous conversions from the last 3 days.
The program uses JSON files to store unit data, which are lightweight and user-friendly, reducing the complexity on file manipulation.
This program supports interactive, command-line and API modes.


## Features
- Convert units across different groups
- Add and remove group of units
- Add and remove types of units for an specific group
- Create and remove aliases for an unit type
- Change base unit conversion of an unit group
- Print conversion history log from the previous 3 days
- Print all groups available
- Print all unit types of an specific group, with their respective aliases


## Motivation & Purpose
This program was created to test and apply all knowledge acquired in "[CS50’s Introduction to Programming with Python](https://pll.harvard.edu/course/cs50s-introduction-programming-python)" course, from Harvard University.


## Table of Contents
- [Description](#description)
- [Features](#features)
- [Motivation & Purpose](#motivation--purpose)
- [Installation](#installation)
- [Usage](#usage)
- [Files Overview](#files-overview)
- [Design Choices](#design-choices)
- [Development Docs](#development-docs)
- [Contributing](#contributing)
- [Future Plans](#future-plans)

## Installation


## Usage


## Files Overview
This program is organized into a `final-project` directory with `data`, `tests` and `unit_converter` subdirectories. The root directory also contains core files and development docs.

- **DATA FILES** (`data/`)
  - [base_units.json](data/base_units.json): contains a relationship between an unit_group and the base unit for that group.
  - [conversion_log.json](data/conversion_log.json): stores all successfull conversions done in the previous 3 days.
  - [month_days.json](data/month_days.json): relates a month's index to its respective name, as well as the number of days in that respective month.
  - [original_units.json](data/original_units.json): contains all unit groups with all unit types for each group and their respective values. Those values don't change, so it's used to refactor all values when users trigger "change-base" action, avoiding precision loss.
  - [unit_aliases.json](data/unit_aliases.json): contains all aliases available for every unit type.
  - [units.json](units.json): contains all unit groups with all unit types for each group and their respective values. Those values change when users trigger "change-base" action, so it's used for conversions.


- **TEST FILES** (`tests/`)
  - [test_api.py](tests/test_api.py): tests all functions in `api.py` file
  - [test_data_manager.py](tests/test_data_manager.py): tests all functions in `data_manager.py` file
  - [test_data_models.py](tests/test_data_models.py): tests all functions in `data_models.py` file
  - [test_utils.py](tests/test_utils.py): tests all functions in `utils.py` file

- **MODULE FILES** (`unit_converter/`)
  - [api.py](unit_converter/api.py): handles the API approach, to allow users to use the program by declaring a `Converter` object class. It will also be used to accomplish the goal of transforming this program into a Library in [`pypi.org`](https://pypi.org/).
  - [data_manager.py](unit_converter/data_manager.py): defines all functions responsible for loading, modifying and saving information on `.json` files.
  - [data_models.py](unit_converter/data_models.py): defines all classes used in the program with all logic responsible for validate those classes' attributes.
  - [utils.py](unit_converter/utils.py): contains all helper functions.


- [project.py](project.py): core file of the program, containing the logic to handle CLI approach, for users that want to use the program through command-line arguments, as well as the logic for an interactive approach. It also contains all files that handles all actions available in the program
- [test_project.py](test_project.py): tests all functions in `project.py` file


## Design Choices
- Using JSON files to manage all data kepts program simple and fast, reducing external dependencies and allowing simplicity on data manipulation. Chose that approach instead of hard-coding in other `.py` files or using databases.
- Chose a modular structure over a single file to improve readability (previous version had `project.py` with over 1000 lines), and to better handling multiple approaches, removing repetitions.
- Besides the interactive mode, which was the first approach that I developed, I also wanted to allow users to access the program through command-line arguments and through API. I decided to keep all three access modes on my final version of the program, giving flexibility and improving UX.
- Created `DataStore` class to globally access all data from those JSON files, instead of manually declaring and accessing them on each file. It kept code cleaner, and improved readability and maintainability.
- Created multiple classes (located in `data_models.py`) to store data and values related to each action. It allowed to centralize all validation logic for each of those values, keeping all other files cleaner with their specific logic.
- Created an unique logic for time conversion, segregated from the default conversion logic, because I wanted to allow multiple input formats. Despite that, I kept all under the same "convert" command so that it doesn't get too segregated, allowing users to focus on which command they want to use, whithout getting overcomplicated.


## Development Docs
- [CHANGELOG.md](CHANGELOG.md): Versions and updates
- [DEVLOG.md](DEVLOG.md): Development  process
- [TODO.md](TODO.md): Features and Goals


## Contributing 
Contributions are welcomed! Follow those steps:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description


## Future Plans
- Publish as a PyPI library
- Refactor `project.py` into modular files
- Add support for more unit groups (e.g. money)