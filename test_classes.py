from unit_converter.api import Converter


converter = Converter()


# converter.groups()

# message = converter.types("length", "a")
# print(message)

# message = converter.history(limit=2, another="a")
# print(message)

# message = converter.convert("length", "m 10")
# print(str(message))

#converter.manage_group("metro", "remove")
#print(f"Result: {result}")

# result = converter.manage_type("temperature", "add new_type 1 1")
# print(f"Result: {result}")

result = converter.change_base("length", "meters")
print(f"Result: {result}")

# result = converter.aliases("length", "remove meters mtr", print_message=True)
# print(f"Result: {result}")