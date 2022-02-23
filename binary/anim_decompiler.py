# anim_decompiler.py
#	decompile animation commands in fire red
#
# written by: Skeli789
#
#

#Data
RomPath = 'rom.gba'
AnimFolderPath = './'
Commands = 'Commands_Python.bsh'
BackgroundDefines = 'backgrounds.bsh'
OffsetDefines = 'locations.bsh'
BanksDefines = 'banks.bsh'
SideDefines = 'sides.bsh'

AnimationName = input('Anim Name: ')
AnimationOffset = int(input('Anim Offset: '),16)

def MoveAnimDecompiler(offset, name):
    output = open(AnimFolderPath + name + '.asm', 'w')
    output.write('@ 0x' + dec2hex(int(offset)) + ' ' + addUnderscore(name) + '_ANIM:\n')
	#output.write('' + addUnderscore(name) + '_ANIM:\n')
    commandlist = CommandListMaker()
    otheroffsets = set()
    otheroffsets2 = set()
    templates = set()
    with open(RomPath, "rb") as binary_file:
        decompileAnim(offset, otheroffsets, templates, binary_file, commandlist, output)
        while otheroffsets != set():
            for loc in otheroffsets:
                decompileAnim(loc, otheroffsets2, templates, binary_file, commandlist, output)
            otheroffsets = set()
            for loc in otheroffsets2:
                decompileAnim(loc, otheroffsets, templates, binary_file, commandlist, output)
            otheroffsets2 = set()
        output.write('\n.align 2')
        for template in templates:
            decompileTemplate(template, binary_file, output)
        
    output.close() 
    print('Decompilation Complete')
        
def decompileAnim(offset, otheroffsets, templates, binary_file, commandlist, output):
        if int(offset) + 0x8000000 in offsetdefinesdict:
            output.write(offsetdefinesdict[int(offset) + 0x8000000] + ':\n')
        else:
            output.write('Loc_' + '0x' + dec2hex(int(offset)) + ':\n')
        binary_file.seek(offset)
        code = '0x0'

        while str(code) != '0x8' and str(code) != '0xF' and str(code) != '0xf':
            binary_file.seek(offset)
            code = hex(binary_file.read(1)[0])
            currentcommand = 'None'
            for command in commandlist:
                if command.num == int(code, 16):
                    currentcommand = command
                    break
            if currentcommand == 'None':
                print('Error with command ' + str(code))
                code = '0x8'
            else:
                output.write('	' + currentcommand.name + ' ')
                offset += 1
                binary_file.seek(offset)
                number = 0
                
#Start Actual Decompilation                
                for a in currentcommand.arglengths:
                    a, b = a, a
                    writecode = ''
                    while b > 0:
                        writecode += dec2hex(binary_file.read(a)[b-1])
                        binary_file.seek(offset)                        
                        b -= 1

#Convert as much as possible to real words
                    if currentcommand.argnames[number] == '"Rom_Address"':
                        otheroffsets.add(int(writecode, 16) - 0x8000000)
                        if int(writecode, 16) in offsetdefinesdict:
                            output.write(offsetdefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    elif currentcommand.argnames[number] == '"Template_Offset"':
                        templates.add(int(writecode, 16) - 0x8000000)
                        if int(writecode, 16) in offsetdefinesdict:
                            output.write(offsetdefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    elif currentcommand.argnames[number] == '"Task_Offset"':
                        if int(writecode, 16) in offsetdefinesdict:
                            output.write(offsetdefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    elif currentcommand.argnames[number] == '"Bank"':
                        if int(writecode, 16) in banksdefinesdict:
                            output.write(banksdefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    elif currentcommand.argnames[number] == '"Bank/Side"':
                        if int(writecode, 16) in sidesdefinesdict:
                            output.write(sidesdefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    elif currentcommand.argnames[number] == '"Background_Num"' or currentcommand.argnames[number] == '"BG_on_Opponent_Side"' or currentcommand.argnames[number] == '"BG_on_Player_Side"' or currentcommand.argnames[number] == '"BG_Contest"':
                        if int(writecode, 16) in backgrounddefinesdict:
                            output.write(backgrounddefinesdict[int(writecode, 16)] + ' ')
                        else:
                            output.write(hex(int(writecode, 16)) + ' ')
                    else:
                        output.write(hex(int(writecode, 16)) + ' ')
                    offset += a
                    binary_file.seek(offset)
                    number += 1

                if command.num == 2 or command.num == 3 or command.num == 31:
                    binary_file.seek(offset-1)
                    for a in range(binary_file.read(1)[0]):
                        binary_file.seek(offset)
                        a, b = 2, 2
                        writecode = ''
                        while b > 0:
                            writecode += dec2hex(binary_file.read(a)[b-1])
                            binary_file.seek(offset)                        
                            b -= 1
                        output.write(hex(int(writecode, 16)) + ' ')
                        offset += a                                       
                else:
                    pass
                output.write('\n')
                
def decompileTemplate(offset, binary_file, output):
    if offset + 0x8000000 in offsetdefinesdict:
        output.write('\n\n' + offsetdefinesdict[offset + 0x8000000] + ':\nobjtemplate ')
    else:
        output.write('\n\nTemplate_' + hex(offset) + ':\nobjtemplate ')
    binary_file.seek(offset)
    for a in range(2):
        code = ''
        for b in range(2):
            binary_file.seek(offset)
            code = dec2hex(int(binary_file.read(2)[b])) + code
        code = '0x' + code + ' '
        output.write(code)
        offset += 2
        binary_file.seek(offset)
    for a in range(5):
        code = ''
        for b in range(4):
            binary_file.seek(offset)
            code = dec2hex(int(binary_file.read(4)[b])) + code
        code = '0x' + removeLeadingZeros(code) + ' '
        output.write(code)
        offset += 4
        binary_file.seek(offset)
    
def CommandListMaker():
    commandlist = []
    with open(Commands, 'r') as file:
        linenum = 0
        for line in file:
            linenum += 1
            errortitle = 'Error in commands file: "' + Commands + '" on line ' + str(linenum) + ': '
            if line != '\n':
                linelist = (line.rstrip()).split(' ')
                commandnum, argnum, arglengths, argnames = 0, 0, [], []
                for a in range(len(linelist)):
                    if a >= 3:
                        if a % 2 == 0:
                            try:
                                arglengths.append(int(linelist[a]))
                            except ValueError:
                                try:
                                    arglengths.append(int(linelist[a], 16))
                                except ValueError:
                                    error = errortitle + 'There was a problem with parsing the argument lengths. Make sure the only space characters are between arguments, and not within argument names.\n'
                                    print(error)
                        else:
                            try:
                                int(linelist[a])
                                error = errortitle + 'There was a problem with parsing the argument names. Make sure the only space characters are between arguments, and not within argument names.\n'
                                print(error)
                            except ValueError:
                                try:
                                    int(linelist[a], 16)
                                    error = errortitle + 'There was a problem with parsing the argument names. Make sure the only space characters are between arguments, and not within argument names.\n'
                                    print(error)
                                except ValueError:
                                    argnames.append(linelist[a])
                                    
                if checkLetters(linelist[0]) == False:
                    error = errortitle + '"' + linelist[0] + '" begins with non-alphabetical characters.\n'
                    print(error)
                    
                try:
                    commandnum = int(linelist[1])
                except ValueError:
                    try:
                        commandnum = int(linelist[1], 16)
                    except ValueError:
                        error = errortitle + '"' + linelist[1] + '" is not a valid command number.\n'
                        print(error)
                        
                try:
                    argnum = int(linelist[2])
                except ValueError:
                    try:
                        argnum = int(linelist[2], 16)
                    except ValueError:
                        error = errortitle + '"' + linelist[2] + '" is not a valid number for argument amount.\n'
                        print(error)
                except IndexError:
                    pass
                
                try:
                    commandlist.append(AnimCommands(linelist[0], commandnum, argnum, arglengths, argnames))
                except IndexError:
                    commandlist.append(AnimCommands(linelist[0], commandnum, 0, [], []))
                          
    return commandlist
            
class AnimCommands:
    def __init__(self, name, num, argnum, arglengths, argnames):
        self.name = name
        self.num = num
        self.argnum = argnum
        self.arglengths = arglengths
        self.argnames = argnames
        
def DefinesDictMaker(DefinesFile):
    definesdict = {}
    with open(DefinesFile, 'r') as file:
        for line in file:
            if line != '\n' and line != '':
                try:
                    key, value = int(line.rstrip().split(', ')[1]), line.rstrip().split(', ')[0]
                except ValueError:
                    key, value = int(line.rstrip().split(', ')[1], 16), line.rstrip().split(', ')[0]
                definesdict[key] = value
    return definesdict

        
DecHexDict = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
def dec2hex(num):
    b = ''
    if num == 0:
        b = '00'
    else:
        while num > 0:
            remainder = num % 16
            if remainder in DecHexDict:
                remainder = DecHexDict[remainder]
            num //= 16
            b = str(remainder) + b
    if len(b) == 1:
        b = '0' + b
    return b

def addUnderscore(string):
    newstring = ''
    for a in string:
        if a == ' ' or a == '-':
            newstring += '_'
        else:
            newstring += a
    return newstring

lowercaseletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
uppercaseletters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def checkLetters(string):
    for a in string:
        if a not in lowercaseletters and a not in uppercaseletters:
            return False
        return True
    
def removeLeadingZeros(string):
    ns, counter = '', False
    for a in string:
        if a == '0' and counter == False:
            pass
        else:
            counter = True
            ns += a
    if ns == '':
        ns = '0'
    return ns

backgrounddefinesdict = DefinesDictMaker(BackgroundDefines)
offsetdefinesdict = DefinesDictMaker(OffsetDefines)
banksdefinesdict = DefinesDictMaker(BanksDefines)
sidesdefinesdict = DefinesDictMaker(SideDefines)

MoveAnimDecompiler(AnimationOffset, AnimationName)