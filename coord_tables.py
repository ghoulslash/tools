import os, sys, argparse, configparser, shutil, subprocess, fnmatch, itertools
import os.path

def print_coords_table(table,offset,n,item):
	print('const struct MonCoords ' + str(table) + '[] =\n{') 
	with open('test.gba', 'r+b') as rom:	
		for i in range(0,n):
			rom.seek(offset)
			size = rom.read(1)[0]
			temp = offset + 1
			rom.seek(temp)
			y_offset = rom.read(1)[0]
			print('[' + str(list[i]) + '] = ' + str(item) + '(' + str(size) + ', ' + str(y_offset) + '),')
			offset += 4
		rom.close()
	print('};')
	
def print_elevation_table(offset, n):
	print('const u8 gEnemyMonElevation[NUM_SPECIES] =\n{') 
	with open('test.gba', 'r+b') as rom:	
		for i in range(0,n):
			rom.seek(offset)
			elev = rom.read(1)[0]
			if (elev > 0):
				print('[' + str(list[i]) + '] = ' + str(elev) + ',')
			offset += 1
		rom.close()
	print('};')

list = [];
with open('species.txt','r') as file:
	for line in file:
		species = str(line.split(' ')[0])
		list.append(species)
		NUM_SPECIES = int(line.split(' ')[1])

# #back coords
offset = 0x235E6C
print_coords_table('gMonBackPicCoords',offset,NUM_SPECIES,'back_pic_coords')
# #front coords
offset = 0x2349CC
print_coords_table('gMonFrontPicCoords',offset,NUM_SPECIES,'front_pic_coords')
# #elevation
offset = 0x23A004
print_elevation_table(offset,412)
