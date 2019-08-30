# ascii2hex.py
#	convert string to fire red hexadecimal byte string
#
# written by: FBI
#
str = input("Ascii: ")
with open("hex_table.txt") as table:
	names = table.read().splitlines()
	
num = len(str)
count = 0
result=""
for x in names:
	for char in x:
		
print(result)
	