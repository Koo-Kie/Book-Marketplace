import ctypes

# Convert the hexadecimal memory address to an integer
memory_address = int("1B7DCB81C4C", 16)
import ctypes


a = 10
memfield = (ctypes.c_int).from_address(id(a))
print(memfield) # c_int(15)
