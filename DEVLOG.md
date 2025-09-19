# Development Log

## [DATE]
**Plans**

**Decisions**

**Challenges**

**Progress**


## [2025-09-01] - Version 0.6.0
**Plans**
- Allow users to convert multiple time unit formats

**Challenges**

**Progress**


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



09-02
aliases
turn back to previous code because current approach was getting too verbose, with repetitive code, and helpers functions to solve new problems that just appeared with my solution.
Thought that probably could have a better way


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