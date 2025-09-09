def zero_division_checker(num):
    if num == 0:
        raise ZeroDivisionError("Can't Divide by zero")