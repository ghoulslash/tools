import os, sys, argparse, configparser, shutil, subprocess, fnmatch, itertools
import os.path
import xlrd

iniparser = configparser.ConfigParser(allow_no_value=True)
iniparser.optionxform = str

with open("config.ini", "r", encoding="UTF-8") as ini:
	iniparser.read_file(ini, "config.ini")
	
free_space = iniparser.get("defines", "free-space", fallback="0x800000")
num_pokes = iniparser.get("defines", "num-pokes", fallback="386")
fs_byte = iniparser.get("defines", "free-space-byte", fallback="255")
fs_byte = int(fs_byte, 16)
table_size = int(num_pokes)*int(16)		# 16 bytes per poke


def find_free_space(size,start):
	with open('test.gba','rb') as rom:
		rom.seek(start)
		curr = rom.read(size)
		return curr

# find word-aligned free space equal to table size
found = 0
ind = 0
start = int(free_space, 16)
while found == 0:
	curr = find_free_space(table_size, start)		# only getting here once
	for i in range(0,table_size):
		if str(curr[i]) != str(fs_byte):
			ind = i+1
	if ind != 0:
		start += ind
		while int(start) % 4 != 0:
			start += 1
	else:
		found = 1
	break

print('Table Start = ' + hex(start) )	
	
# loop through compatabilities
table = xlrd.open_workbook("./compat.xlsx")
table = table.sheet_by_index(0)

if (table.ncols-1) != int(num_pokes):
	print('Error :: Number of Columns does not match Number of Pokemon')
	exit()
	
compat_table = ''
for i in range(1,int(num_pokes)):			# loop through column number
	tms = [0] * 128		#base bitfield
	for j in range(1,table.nrows):			# loop through row
		temp = table.cell_value(j,i)
		if temp == int(1):
			ind = int(j)-1
			tms[ind] = 1
	first_word = list(reversed(tms[0:32]))
	second_word = list(reversed(tms[32:64]))
	third_word = list(reversed(tms[64:96]))
	fourth_word = list(reversed(tms[96:128]))
	
	#convert lists to binary strings
	tms32 = ''
	tms64 = ''
	tms96 = ''
	tms128 = ''
	for i in first_word:
		tms32 += str(i)
	for i in second_word:
		tms64 += str(i)
	for i in third_word:
		tms96 += str(i)
	for i in fourth_word:
		tms128 += str(i)

	#get big endian hex values	
	hex32_fwd = '{:0{}X}'.format(int(tms32, 2), len(tms32) // 4)
	hex64_fwd = '{:0{}X}'.format(int(tms64, 2), len(tms64) // 4)
	hex96_fwd = '{:0{}X}'.format(int(tms96, 2), len(tms96) // 4)
	hex128_fwd = '{:0{}X}'.format(int(tms128, 2), len(tms128) // 4)

	#transform into little endian hex
	hex32 = ''
	hex64 = ''
	hex96 = ''
	hex128 = ''
	for i in range(0,8):
		if i % 2 == 1:	#odd num
			x = 8 - i		#odd index
		else:
			x = 6 - i		#even index
		hex32 += str(list(hex32_fwd)[x])
		hex64 += str(list(hex64_fwd)[x])
		hex96 += str(list(hex96_fwd)[x])
		hex128 += str(list(hex128_fwd)[x])
	compat_table += (hex32 + hex64 + hex96 + hex128)

# convert to list of bytes for rom import
btable = [0] * table_size
ind = 0
for i in range(0,int(table_size/2)):
	temp = compat_table[ind] + compat_table[ind+1]
	btable[i] = int(temp,16)
	ind += 2

# write to rom
with open('test.gba', 'r+b') as rom:
	rom.seek(start)
	rom.write(bytes(btable))
	rom.close()
	

