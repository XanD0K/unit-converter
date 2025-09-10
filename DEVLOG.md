# Development Log

## [DATE]
**Plans**

**Decisions**

**Challenges**

**Progress**



## [2025-08-28] - Version 0.0.1

**Goals**
- Implement the first functional structure for a converter program

**What Was Done**
- Defined a `units` dictionary



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