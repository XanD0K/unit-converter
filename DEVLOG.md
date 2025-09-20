# Development Log

## [DATE]
**Plans**

**Challenges**

**Progress**



## [2025-09-03] - Version 0.7.0
**Plans**
- Add aliases to all actions to improve UX
- Decided to remove `while` loops that kept user inside each input, keeping only the `while` loop in `get_action`, so user can trigger multiple acctions in a single session

**Challenges**
- `argparse` module doesn't have a direct interaction between argument's name and argument's aliases. I can't just check for its name. I also need to check for its aliases

**Progress**
- Created `unit_alises.json` file, that contain all aliases for each unit_type. Also created `manage_aliases` function that allows users to add and remove aliases from that file
- Created `resolve_aliases` function to get user's input, either the full unit name or its alias, and outputs its respective name
- Changed `handle_cli` to also allow aliases manipulation through CLI


## [2025-09-01] - Version 0.6.0
**Plans**
- Allow users to input multiple time unit formats

**Challenges**
- Deal with multiple formats means deal with different users inputs

**Progress**
- Created `days_to_month.json` file to strore a relationship between month's name and the number of days on that month
- Created `converter_time` function to handle multiple formats for time conversion (e.g. seconds minutes 10, 17:28:36 04:15:22 seconds, JAN NOV minutes, 2019-11-04 2056-04-28 days)
- Created `parse_time_input`, `check_time_is_none` and `parse_date_input` helper functions that use `re` and `datetime` modules to assist on time conversion
- Changed `add_to_log` function to also accept multiple time formats
- Changed `print_history` function to print different messages based on conversion time format
- Changed `handle_cli` function to also accept multiple formats for time conversion


## [2025-08-31] - Version 0.5.0
**Plans**
- Allow users to see previous conversions

**Progress**
- Created `conversion_log.json` file to keep track of all past conversions user has made
- Created `add_to_log` function to add successfull conversions to that new `conversion_log.json` file
- Created `history` command, so user can access and print previous conversions


## [2025-08-29] - Version 0.4.0
**Plans**
- Keep current interactive mode, and also allow users to access the program through command-line arguments
- Allow users to trigger an action in CLI with aliases, keeping code less verbose

**Challenges**
- Handle `argparse` module and how to configure command-line arguments
- "add" action was more complex to implement in CLI

**Progress**
- Created `base_units.json` file to keep track of base units for every unit group
- Created `validate_dictionaries` function to validate both `.json` files before opening and accessing them
- Created `handle_cli` function to deal with all CLI logic


## [2025-08-28] - Version 0.3.0
**Plans**
- Make code cleaner by creating multiple functions, one for each action

**Challenges**
- Temperature units needed an improved logic
- All my conversion outputs were bad formatted, without punctuations and with trailling zeroes

**Progress**
- Removed actions from `main`, and created specific functions to deal with each action: `add_logic`, `add_new_group` and `conversion_logic`
- To handle temperature units, I also created `converter_temp` to conver temperature units, and `add_temp_logic` to add temperature unit types
- Created `format_value` function to handle trailling zeroes


## [2025-08-27] - Version 0.2.0
**Plans**
- Improve program by handling exceptions and keeping user inside of it
- Segregate files, improving user's UX and making `project.py` file cleaner
- Create multiple actions

**Progress**
- Created introductory messages with instructions
- Implemented and infinite loop to keep user inside the program, until he decides do quit it
- Moved `units` dictionary to `units.json` file, keeping `project.py` cleaner
- Removed `try-except` blocks from all functions, centralizing errors handling in `main`
- Created multiple actions in `main`, allowing users not only to convert values, but to print all unit groups, print all unit types for a specific group and add unit types.


## [2025-08-26] - Version 0.1.0
**Plans**
- Implement the first functional structure for a converter program, starting with the basics and incrementing it gradually

**Challenges**
- Trying to figure out what to do, and how to accomplish it

**Progress**
- Create a `units` dictionary, with all unit groups and unit types, and their respective values based on Internation System of Units (SI)
- Implemented the core logic with `get_amount`, `get_unit_group` `get_converter_unit` and `converter` functions





09-04
changed
def parse_date_input(time_str):
    """Gets user's input of a date, and outputs the year, month and day"""
    if matches := re.search(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", time_str):


09-09
segregating project.py into multiple files, raising error about variables, specially global variables realated to ".json" files
Decided do go with a "data class", for easy access and passing around multiple functions and files


09-16
Changed Converter methods in api.py file  so that it takes user's input as a single argument, and I strip it, instead of passing multiple arguments to the function