#!/usr/bin/python3
# 
# convert_metatile_attribytes.py
#   converts FR tile attribute .bin file to EM
#
# input:
#   ./convert_metatile_attribytes.py <tileset dir name> <primary vs. secondary>
#       eg. ./convert_metatile_attribytes.py primary inside
#
# output: metatile_attributes_new.bin
#
from sys import argv
import os, subprocess, struct

NUM_TILES_IN_PRIMARY = 640
NUM_TILES_TOTAL = 1024
NUM_METATILES_IN_PRIMARY = 640
NUM_METATILES_TOTAL = 1024

def create_new_behavior(path):
    file = os.sep.join([path, 'metatile_attributes.bin'])
    num = int(os.path.getsize(file) / 4)
    
    with open(file, 'rb') as f:
        new_data = bytearray(num * 2)
        data = f.read(num * 4)
        for i in range(0, num):
            behavior = data[i * 4]
                    
            new_data[i * 2] = behavior
            bg = data[i * 4 + 3]
            if bg & 0x20 == 0x20:
                bg = 0x10
            new_data[i * 2 + 1] = bg

    with open(os.sep.join([path, 'metatile_attributes_new.bin']), 'wb+') as f:
        f.write(new_data)
    
if __name__ == '__main__':
    path = os.sep.join([os.curdir, 'data', 'tilesets', str(argv[1]), argv[2]])
    create_new_behavior(path)
    exit()
    