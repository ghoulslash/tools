# extract_images.py
#   use 'dd' to extract sprite front and back, normal and shiny pals from a rom
#   NOTE: assumes sprites were inserted using advanced series order: FRONT_PIC, NORMAL_PAL, BACK_PIC, SHINY_PAL. If this is not the case, the image sizes will be messed up
#
#   Config:
#       1. place python script somewhere
#       2. place your rom in another folder somewhere (ideally the same folder) and update path name of ROM
#       2.5 update FRONT_SPRITE_TABLE, etc to the correct addresses of your sprite tables. They are set to the default FR options
#       3. (optional) get your include/constants/species.h file location path for SPECIES_HEADER. Default assumes you've put extract_images.py in the main decomp directory. If the path/file is incorrect or doesn't exist, the image data will be placed in a directory with just the species number
#       4. run "py extract_images.py" from command line. Input a specific species number, or "0" for range zero to another input value
#       5. the files will be .gbapal.lz and .4bpp.lz. These images will compile for your game, but in order to get the .png and .pal images you will need to do more command line work (sadly, access is denied to these tools inside the subprocess command)
#           from the main decomp dir:
#               tools/gbagfx/gbagfx <to_file>/normal.gbapal.lz <to_file>/normal.gbapal
#               tools/gbagfx/gbagfx <to_file>/normal.gbapal <to_file>/normal.pal
#               tools/gbagfx/gbagfx <to_file>/shiny.gbapal.lz <to_file>/shiny.gbapal
#               tools/gbagfx/gbagfx <to_file>/shiny.gbapal <to_file>/shiny.pal
#               tools/gbagfx/gbagfx <to_file>/front.4bpp.lz <to_file>/front.4bpp
#               tools/gbagfx/gbagfx <to_file>/front.4bpp <to_file>/front.png -width 8 -palette <to_file>/normal.gbapal
#               tools/gbagfx/gbagfx <to_file>/back.4bpp.lz <to_file>/back.4bpp
#               tools/gbagfx/gbagfx <to_file>/back.4bpp <to_file>/back.png -width 8 -palette <to_file>/shiny.gbapal
#
#
import os, sys, argparse, configparser, shutil, subprocess, fnmatch, itertools
import os.path

ROM = 'test.gba'
SPECIES_HEADER = './/include//constants//species.h'
FRONT_SPRITE_TABLE = int(0x2350AC)
BACK_SPRITE_TABLE = int(0x23654C)
NORMAL_PAL_TABLE = int(0x23730C)
SHINY_PAL_TABLE = int(0x2380CC)
   

def ExtractPointer(byteList: [bytes]):
    pointer = 0
    for a in range(len(byteList)):
        pointer += (int(byteList[a])) << (8 * a)

    return pointer

def main(species):
    with open(ROM, 'r+b') as rom:
        #front sprite address
        rom.seek(FRONT_SPRITE_TABLE + 8 * species)
        FRONT_PIC_OFFSET = ExtractPointer(rom.read(3))
        #back sprite address
        rom.seek(BACK_SPRITE_TABLE + 8 * species)
        BACK_PIC_OFFSET = ExtractPointer(rom.read(3))
        #normal pal address
        rom.seek(NORMAL_PAL_TABLE + 8 * species)
        NORMAL_PAL_OFFSET = ExtractPointer(rom.read(3))
        #shiny pal address
        rom.seek(SHINY_PAL_TABLE + 8 * species)
        SHINY_PAL_OFFSET = ExtractPointer(rom.read(3))
        
        # assuming advanced series template!! insertion order is FRONT_PIC, NORMAL_PAL, BACK_PIC, SHINY_PAL
        FRONT_SIZE = int(NORMAL_PAL_OFFSET - FRONT_PIC_OFFSET)
        BACK_SIZE = int(SHINY_PAL_OFFSET - BACK_PIC_OFFSET)
        PAL_SIZE = int(40)
        
        # get species name for directory - this can certainly be optimized
        dirName = str(species)
        if os.path.isfile(SPECIES_HEADER):
            with open(SPECIES_HEADER,'r') as file:
                for line in file:
                    if line.split(' ')[0] == '#define':
                        if line.split(' ')[1].startswith("SPECIES_"):
                            if int(line.split(' ')[len(line.split(' '))-1]) == int(species):
                                dirName = str(line.split(' ')[1]).lower().replace("species_","")
                                break
        
        # make directory if doesn't exist yet
        if not os.path.isdir(dirName):
            os.mkdir(dirName)
        
        process = 'dd if=' + ROM + ' of=' + dirName + '//normal.gbapal.lz' + ' bs=1' + ' skip=' + str(NORMAL_PAL_OFFSET) + ' count=' + str(PAL_SIZE)
        subprocess.call(process)
        
        process = 'dd if=' + ROM + ' of=' + dirName + '//shiny.gbapal.lz' + ' bs=1' + ' skip=' + str(SHINY_PAL_OFFSET) + ' count=' + str(PAL_SIZE)
        subprocess.call(process)
        
        process = 'dd if=' + ROM + ' of=' + dirName + '//front.4bpp.lz' + ' bs=1' + ' skip=' + str(FRONT_PIC_OFFSET) + ' count=' + str(FRONT_SIZE)
        subprocess.call(process)
        
        process = 'dd if=' + ROM + ' of=' + dirName + '//back.4bpp.lz' + ' bs=1' + ' skip=' + str(BACK_PIC_OFFSET) + ' count=' + str(BACK_SIZE)
        subprocess.call(process)
    
        # access denied to tools/gbagfx/gbagfx sadly..
        #process = '..\gbagfx\gbagfx.exe .\pokemon_graphics\normal.gbapal.lz .\pokemon_graphics\normal.gbapal'
        #print(process)
        #subprocess.call(process)
    
species = int(input('Species Number: '))
if species == 0:
    count = int(input('Species Count: '))
    for i in range(0,count):
        main(i)
else:
    main(species)
 
