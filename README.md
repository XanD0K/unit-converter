# UnitConverter
#### Video Demo:  <URL HERE>


## Motivation & Purpose
This program was created to test and apply all knowledge acquired in "[CS50’s Introduction to Programming with Python](https://pll.harvard.edu/course/cs50s-introduction-programming-python)" course, from Harvard University.


## Description
This program has the purpose of converting units from different groups: "length", "time", "mass", "temperature", "volume", "area" and "speed".
In addition to that, users can create and remove groups and types of units, as well as aliases for any unit type.
Users also have the ability to change the base unit of any group, which changes the conversion factor of all unit types in that specific group.
Lastly, he can also access the history log, which contains all previous conversions from the last 3 days.
The program uses JSON files to store unit data, which are lightweight and user-friendly, reducing the complexity on file manipulation.
This program supports interactive, command-line and API modes.


## Features
- Convert units across different groups
- Add and remove group of units
- Add and remove types of units from a specific group
- Create and remove aliases from an unit type
- Change conversion base unit of an unit group
- Print conversion history log from the previous 3 days (default, 10 entries)
- Print all groups available
- Print all unit types from an specific group, with their respective aliases


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
UnitConverter supports three modes: command-line (CLI), interactive, and API. On all approaches, users will have 8 actions available, each of which with its respective aliases. Bellow I'll describe all modes available, and how to use each command on that mode, with its alias and usage example:

### Interactive Mode
Enter `python project.py` to launch the interactive menu with a guided experience. You just need to follow the instructions:
- **Groups** (`groups` or `g`)
  - Output: `Groups: length, time, mass, temperature, volume, area, speed`
- **Types** (`types` or `t`)
  - Enter: `length`
  - Output: 
  ```
  'length' units: meters ('m', 'meter', 'metre', 'metres'), centimeters ('cm', 'centimeter', 'centimetre', 'cetimetres'), millimeters ('mm', 'millimeter', 'millimetre', 'millimetres'), kilometers ('km', 'kilometer', 'kilometre', 'kilometres'), feet ('ft', 'foot'), inches ('in', 'inch'), yards ('yd', 'yds', 'yard'), miles ('mi', 'mile'), nautical_miles ('nmi', 'nm', 'nautical_mile')
  ```
- **History** (`history` or `h`)

  On interactive mode, it will always prints up to 10 entries, with no option to limit this number 
  - Output: 
  ```
  36.5 celsius = 97.7 fahrenheit (Group: temperature)
  5.0 kilograms = 0.005 tonne (Group: mass)
  10.0 liters = 42.26766 cup (Group: volume)
  10.0 meters = 10.93613 yards (Group: length)
  365.0 days between jan dec (Group: time)
  10.0 meters = 10.93613 yards (Group: length)
  1.0 minutes = 60.0 seconds (Group: time)
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```
- **Convert** (`convert` or `c`)
  - Enter: `length`, `meters`, `feet`, `5`
  - Output: `5.0 meters = 16.4042 feet`
- **Manage Groups** (`manage-group` or `mg`)
  - Enter: `add`, `new_group`, `new_base_unit`
  - Output: `You've just created a 'new_group' group, with 'new_base_unit' as its base unit!`
- **Manage Types** (`manage-type` or `mt`)
  - Enter: `length`, `add`, `new_type`, `2.4`
  - Output: `A new unit type was added on 'length' group: new_type = 2.4`
- **Aliases** (`aliases` or `a`)
  - Enter: `length`, `meters`, `add`, `mtr`
  - Output: `Alias successfully added! New alias for 'meters': 'mtr'`
- **Change Base** (`change-base` or `cb`)
  - Enter: `length`, `miles`
  - Output: `You've just changed the base unit from 'length' group, to 'miles'!`


### Command-Line Interface (CLI)
On CLI approach, follow the usage examples bellow to understand how to use each action. Follow the instructions and the position of each argument to prevent triggering any error.
- **Groups** (`groups`, `g`)
  - Enter: `python .\project.py groups` or `python .\project.py g`
  - Output: `Groups: length, time, mass, temperature, volume, area, speed`

- **Types** (`types`, `t`)
  - Enter`python .\project.py types length` or `tpython .\project.py t length`
  - Output: 
  ```
  'length' units: meters ('m', 'meter', 'metre', 'metres'), centimeters ('cm', 'centimeter', 'centimetre', 'cetimetres'), millimeters ('mm', 'millimeter', 'millimetre', 'millimetres'), kilometers ('km', 'kilometer', 'kilometre', 'kilometres'), feet ('ft', 'foot'), inches ('in', 'inch'), yards ('yd', 'yds', 'yard'), miles ('mi', 'mile'), nautical_miles ('nmi', 'nm', 'nautical_mile')
  ```

- **History** (`history`, `h`)

  On CLI mode, users can specify a limit(`--limit` or `-l`), changing the default limit of 10 entries to any limit they want.
  - Enter: `python .\project.py history` or `python .\project.py h`
  - Output: 
  ```
  36.5 celsius = 97.7 fahrenheit (Group: temperature)
  5.0 kilograms = 0.005 tonne (Group: mass)
  10.0 liters = 42.26766 cup (Group: volume)
  10.0 meters = 10.93613 yards (Group: length)
  365.0 days between jan dec (Group: time)
  10.0 meters = 10.93613 yards (Group: length)
  1.0 minutes = 60.0 seconds (Group: time)
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```

  - Enter: `python .\project.py history --limit 3` or `python .\project.py h --limit 3`
  - Output: 
  ```
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```

  - Enter: `python .\project.py history -l 3` or `python .\project.py h -l 3`
  - Output: 
  ```
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```

- **Convert** (`convert`, `c`)
  - Enter: `python .\project.py convert length meters feet 5` or `python .\project.py c length meters feet 5`
  - Output: `5.0 meters = 16.4042 feet`

- **Manage Groups** (`manage-group` or `mg`)
  - Enter: `python .\project.py manage-group add new_group new_base_unit` or `python .\project.py mg add new_group new_base_unit`
  - Output: `You've just created a 'new_group' group, with 'new_base_unit' as its base unit!`
  - Enter: `python .\project.py manage-group remove new_group` or `python .\project.py mg remove new_group`
  - Output: `Group 'new_group' successfully removed!`

- **Manage Types** (`manage-type` or `mt`)
  - Enter: `python .\project.py manage-type length add new_type 2.4` or `python .\project.py mt length add new_type 2.4`
  - Output: `A new unit type was added on 'length' group: new_type = 2.4`
  - Enter: `python .\project.py manage-type length remove new_type` or `python .\project.py mt length remove new_type`
  - Output: `'new_type' was removed from 'length'`

  When adding a new type in the `temperature` group, user needs to insert a factor (`--factor`) and an offset (`--offset`)
  - Enter: `python .\project.py manage-type temperature add new_type --factor 1 --offset 1` or `python .\project.py mt temperature add new_type --factor 1 --offset 1`
  - Output: `A new unit type was added on 'temperature' group: new_type = [1, 1]`
  - Enter: `python .\project.py manage-type temperature remove new_type` or `python .\project.py mt temperature remove new_type`
  - Output: `'new_type' was removed from 'temperature'`
  
- **Aliases** (`aliases` or `a`)
  - Enter: `python .\project.py aliases length meters add mtr` or `python .\project.py a length meters add mtr`
  - Output: `Alias successfully added! New alias for 'meters': 'mtr'`
  - Enter: `python .\project.py aliases length meters remove mtr` or `python .\project.py a length meters remove mtr`
  - Outpur: `'mtr' successfully removed from 'meters'!`

- **Change Base** (`change-base` or `cb`)
  - Enter: `python .\project.py change-base length miles` or `python .\project.py cb length miles`
  - Output: `You've just changed the base unit from 'length' group, to 'miles'!`


### API
When accessing the program through API, first users will need to declare a class object, which will allow to call `Converter` class' methods: 
```
from unit_converter.api import Converter
converter = Converter()
```

The `convert`, `manage-group`, `manage-type`, `aliases` and `change-base` methods have a `print_message` attribute which is set to `False` by default. It means that those actions won't print any message when called. To get the output message, users have 2 options:
1. Call the method with `print_message` set to `True`, which will output the message where it was called.
2. Assign the method to a variable, with `print_message` attribue set to `False`. It allows users to choose where to print the output message.

Also, if users don't want the output message, just let `print_message` set to `False` and don't assign it to any variable. THe method will be triggered, but no message will be displayed. Wherease, if users set `print_message` set to `True` and also assign it to a variable, it will print the message where it was called, and users will also have that same message stored in a variable, with the possibility to call it wherever they want.

The `groups`, `types` and `history` methods don't have that `print_message` attribute. Those commands always need the result to be assigned to a variable so that the output message can be displayed.

- **Groups** (`groups`, `g`)
  - Enter:
  ```
  message = converter.groups()
  print(message)
  ```
  - Output: `Groups: length, time, mass, temperature, volume, area, speed`

- **Types** (`types`, `t`)
  - Enter:
  ```
  message = converter.types("length")
  print(message)
  ```
  - Output: 
  ```
  'length' units: meters ('m', 'meter', 'metre', 'metres'), centimeters ('cm', 'centimeter', 'centimetre', 'cetimetres'), millimeters ('mm', 'millimeter', 'millimetre', 'millimetres'), kilometers ('km', 'kilometer', 'kilometre', 'kilometres'), feet ('ft', 'foot'), inches ('in', 'inch'), yards ('yd', 'yds', 'yard'), miles ('mi', 'mile'), nautical_miles ('nmi', 'nm', 'nautical_mile')
  ```

- **History** (`history`, `h`)

  On API mode, user can specify a limit(`limit=`), changing the default limit of 10 entries to whatever limit he wants.
  - Enter: 
  ```
  message = converter.history()
  print(message)
  ```
  - Output: 
  ```
  36.5 celsius = 97.7 fahrenheit (Group: temperature)
  5.0 kilograms = 0.005 tonne (Group: mass)
  10.0 liters = 42.26766 cup (Group: volume)
  10.0 meters = 10.93613 yards (Group: length)
  365.0 days between jan dec (Group: time)
  10.0 meters = 10.93613 yards (Group: length)
  1.0 minutes = 60.0 seconds (Group: time)
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```

  - Enter: 
  ```
  message = converter.history(limit=3)
  print(message)
  ```
  - Output: 
  ```
  1.0 decades 1.0 centuries 1.0 months 1.0 hours = 3,473,931,600.0 seconds (Group: time)
  5.0 meters = 16.4042 feet (Group: length)
  5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds (Group: time)
  ```

- **Convert** (`convert`, `c`)

  On API mode, user can choose if the `convert` method will output only the result of the conversion, or the output message. It is set by the value of the `print_message` attribute.
  - Enter: 
  ```
  message = converter.convert("length", "meters feet 5")
  print(message)
  ```
  - Output: `16.4042 feet`

  - Enter: 
  ```
  message = converter.convert("length", "meters feet 5", print_message=True)
  print(message)
  ```
  - Output: `5.0 meters = 16.4042 feet`

- **Manage Groups** (`manage-group` or `mg`)
  - Enter: `message = converter.manage_group("new_group", "add new_base_unit", print_message=True)` or 
  ```
  message = converter.manage_group("new_group", "add new_base_unit")
  print(message)
  ```
  - Output: `You've just created a 'new_group' group, with 'new_base_unit' as its base unit!`
  - Enter: `converter.manage_group("new_group", "remove", print_message=True)` or
  ```
  message = converter.manage_group("new_group", "remove")
  print(message)
  ```
  - Output: `Group 'new_group' successfully removed!`

  
- **Manage Types** (`manage-type` or `mt`)
  - Enter: `converter.manage_type("length", "add new_type 2.4", print_message=True)` or
  ```
  message = converter.manage_type("length", "add new_type 2.4")
  print(message)
  ```
  - Output: `A new unit type was added on 'length' group: new_type = 2.4`
  - Enter: `converter.manage_type("length", "remove new_type", print_message=True)` or 
  ```
  message = converter.manage_type("length", "remove new_type")
  print(message)
  ```
  - Output: `'new_type' was removed from 'length'`

  When adding a new type in the `temperature` group, user needs to insert a factor (`--factor`) and an offset (`--offset`)
  - Enter: `converter.manage_type("temperature", "add new_type 1 1", print_message=True)` or
  ```
  message = converter.manage_type("temperature", "add new_type 1 1")
  print("message")
  ```
  - Output: `A new unit type was added on 'temperature' group: new_type = [1.0, 1.0]`
  - Enter: `converter.manage_type("temperature", "remove new_type", print_message=True)` or
  ```
  message = converter.manage_type("temperature", "remove new_type")
  print(message)
  ```
  - Output: `'new_type' was removed from 'temperature'`
  
- **Aliases** (`aliases` or `a`)
  - Enter: `converter.aliases("length", "add meters mtr", print_message=True)` or
  ```
  message = converter.aliases("length", "add meters mtr")
  print(message)
  ```
  - Output: `Alias successfully added! New alias for 'meters': 'mtr'`
  - Enter: `converter.aliases("length", "remove meters mtr", print_message=True)` or
  ```
  message = converter.aliases("length", "remove meters mtr")
  print(message)
  ```
  - Outpur: `'mtr' successfully removed from 'meters'!`

- **Change Base** (`change-base` or `cb`)
  - Enter: `converter.change_base("length", "mile", print_message=True)`
  ```
  message = converter.change_base("length", "mile")
  print(message)
  ```
  - Output: `You've just changed the base unit from 'length' group, to 'miles'!`


#### Date & Time Conversion
This program handles date and time conversion in a more robust way, so I'll devote a specific section on this `README.md` file just to explain all possibilites users have available. On Interactive mode, enter `convert` or `c` and then `time` as the unit group, and follow the guided instructions. For API approach, I'll give examples that will display the full output message, but keep in mind that you can directly call the `convert` class method with `print_message` set to `False`, which will jsut print the result.

- **Simple Unit Type Conversion**
  Users can convert from different unit types. 
  Usage: `<unit_type> <unit_type> <amount>`
  - Enter: `minutes seconds 1` or `python .\project.py convert time minutes seconds 1` or 
  ```
  message = converter.convert("time", "minutes seconds 1", print_message=True)
  print(message)
  ```
  - Output: `1.0 minutes = 60.0 seconds`

- **Complex Unit Type Conversion**

  Users can input multiple unit types to convert to a specific unit type. That approach demmands taht users inputs at least 2 `(<amount> <unit_type>)` blocks to convert from. If input format consists only of one unit type, use previous approach! 

  Usage: `<amount> <unit_type> (<amount> <unit_type>) <unit_type>`
  - Enter: `5 years 10 months 10 days 8 hours 56 minutes seconds` or `python .\project.py convert time 5 years 10 months 10 days 8 hours 56 minutes seconds` or 
  ```
  message = converter.convert("time", "5 years 10 months 10 days 8 hours 56 minutes seconds", print_message=True)
  print(message)
  ```
  - Output: `5.0 years 10.0 months 10.0 days 8.0 hours 56.0 minutes = 184,604,160.0 seconds`

- **Simple Time Conversion**

  User can convert a specific time to a specific unit type. For that conversion, users aren't limit in the 24h pattern. They can use any value they want.

  The time input need to follow that pattern: `HH:MM:SS`. If no group of units, its `:` sign is still need. User either declare the empty value as zeroes, or leave the initial `:` sign to declare the empty value.
  Usage: `<TIME> <TIME> <unit_type>`
  - Enter: `17h:28m:36s seconds` or `python .\project.py convert time 17h:28m:36s seconds` or 
  ```
  message = converter.convert("time", "17h:28m:36s seconds", print_message=True)
  print(message)
  ```
  - Output: `There are 62,916.0 seconds in 17h:28m:36s`






## Files Overview
This program is organized into a `unit-converter` directory with `data`, `tests` and `unit_converter` subdirectories. The root directory also contains core files and development docs.

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
- In API mode, all actions return the output message, without displaying it! It means that when a class method is called, the action is triggered, but is up to the users to decide if they want to print it. By assigning that method call to a variable, they can also decide where they want to print that message.

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