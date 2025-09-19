from unit_converter.api import Converter


converter = Converter()

#converter.groups()

#message = converter.types("lngth")
#print(message)

#message = converter.history(limit="2a")
#print(message)

message = converter.convert("lenth", "m yd 5")
print(str(message))



#result = converter.manage_group("metro", "add metroo ", print_message=True)
#print(f"Result: {result}")

#result = converter.manage_type("metro", "metru add 0.00001", print_message=True)
#print(f"Result: {result}")

#result = converter.change_base("metro", "metroo", print_message=True)
#print(f"Result: {result}")

#result = converter.aliases("metro", "metroo remove mo", print_message=True)
#print(f"Result: {result}")
