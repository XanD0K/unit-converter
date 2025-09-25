# Unit Converter
#### Video Demo:  <URL HERE>


## Description:
This program has the purpose of converting different units. User can choose from a variety of groups: "length", "time", "mass", "temperature", "volume", "area" and "speed".
In addition to that, user has the ability to create and to remove their own groups and types of units, as well as aliases for any unit type.
User also has the ability to change the base unit of any group, and to access the history log, which contains all previous conversions from the last 3 days.


## Motivation & Purpose
This program was created to test and apply all knowledge acquired in "CS50’s Introduction to Programming with Python" course (cs50p), from Harvard University.


## Table of Contents
- [Description](#description)
- [Motivation & Purpose](#fmotivation--purpose)
- [Files Overview](#files-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Development Docs](#development-docs)



## Files Overview
- [base_units.json](data/base_units.json): file that contain a relationship between an unit_group and the base unit for that group.
- [conversion_log.json](data/conversion_log.json): file that stores all successfull conversions done in the previous 3 days.
- [month_days.json](data/month_days.json): file that relates a month's index to its respective name, as well as the number of days in that respective month.
- [original_units.json](data/original_units.json): file that contains all unit groups with all unit types for each group and their respective values. Those values don't change, so it's used to refactor all values when user triggers "change-base" action, avoiding precision loss.
- [unit_aliases.json](data/unit_aliases.json): file that contains all aliases available for every unit type.
- [units.json](units.json): file that contains all unit groups with all unit types for each group and their respective values. Those values change when user triggers "change-base" action, so it's used for conversions.


- [project.py](project.py): core file of the program, containing the logic to handle CLI approach, for users that want to use the program throught command-line arguments, as well as the logic for an interactive approach. It also contains all files that handles all actions available in thr program

- [test_project.py](test_project.py): file used to test the all functions in `project.py` file




## Installation


## Usage


## Development Docs
- [CHANGELOG.md](CHANGELOG.md): Versions and updates
- [DEVLOG.md](DEVLOG.md): Development  process
- [TODO.md](TODO.md): Features and Goals