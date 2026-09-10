#!/usr/bin/env python3
######################################################################
#
# Be sure to use python3...
#
# This is just an example to get you started if you are having
# difficulty starting the assignment. It is by no means the most
# efficient way to implement this disassembler, however, it is one
# that can easily be followed and extended to complete the requirements
#
# You may want to import other modules, but certainly not required
# This implements linear sweep..this can be modified to implement
# recursive descent as well
#
######################################################################
import sys
import argparse

#
# Key is the opcode
# value is a list of useful information
GLOBAL_OPCODE_MAP = {
    # OPCODE : [ mnemonic or None if requires opcode extension, hasModRMByte,
    # OpEn, OpcodeExtension dictionary ],
    0x05 : ['add eax, ', False, 'id', None ],
    0x01 : ['add ', True, 'mr', None], 
    0x03 : ['add ', True, 'rm', None],
    0x25 : ['and eax, ', False, 'i', None ],
    0x21 : ['and ', True, 'mr', None],
    0x23 : ['and ', True, 'rm', None ],
    0xE8 : ['call ', False, 'd', None],
    0x3D : ['cmp eax, ', False, 'i', None],
    0x39 : ['cmp ', True, 'mr', None ],
    0x3B : ['cmp ', True, 'rm', None], 
    0x48 : ['dec ', False, 'o', None ],
    0x40 : ['inc ', False, 'o', None ],
    0xEB : ['jmp ', False, 'd', None], 
    0xE9 : ['jmp ', False, 'd', None],
    0x74 : ['jz ', False, 'd', None], 
    #0x0F 0x84 : ['jz ', False, 'd', None],
    0x75 : ['jnz ', False, 'd', None ],
    #0x0F 0x85 : ['jnz ', False, 'd', None], 
    0x8D : ['lea ', True, 'rm', None],
    0xA1 : ['mov eax, ', False, 'fd', None ],
    0xA3 : ['mov ', False, 'td', None], 
    0xB8 : ['mov ', False, 'oi', None],
    0x89 : ['mov ', True, 'mr', None], 
    0x8B : ['mov ', True, 'rm', None],
    0xA5 : ['movsd ', False, 'zo', None ],
    0x90 : ['nop ', False, 'zo', None], 
    0x0D : ['or eax, ', False, 'i', None ],
    0x09 : ['or ', True, 'mr', None],
    0x0B : ['or ', True, 'rm', None ],
    0x58 : ['pop ', False, 'o', None],
    0x50 : ['push ', False, 'o', None], 
    0x68 : ['push ', False, 'i', None],
    0x6A : ['push ', False, 'i', None ],
    #0xF2 0xA7: ['repne ', False, 'zo', None], 
    0xCB : ['retf ', False, 'zo', None],
    0xCA : ['retf ', False, 'i', None ],
    0xC3 : ['retn ', False, 'zo', None], 
    0xC2 : ['retn ', False, 'i', None],
    0x2D : ['sub eax, ', False, 'id', None ],
    0x29 : ['sub ', True, 'mr', None],
    0x2B : ['sub ', True, 'rm', None ],
    0xA9 : ['test eax, ', False, 'i', None], 
    0x85 : ['test ', True, 'mr', None ],
    0x35 : ['xor eax, ', False, 'i', None],
    0x31 : ['xor ', True, 'mr', None ],
    0x33 : ['xor ', True, 'rm', None], 

    # Codes needing opcode extension
    0x81 : [ None, True, 'mi', { 0: 'add', 1: 'or', 2: 'adc', 3: 'sbb', 4:
                                'and', 5: 'sub', 6: 'xor', 7: 'cmp' } ],
    0x8F : [ None, True, 'm', { 0: 'pop' } ],
    0xC7 : [ None, True, 'mi', { 0: 'mov' } ],
    0xF7 : [ None, True, 'rm', { 0: 'test', 2: 'not', 3: 'neg', 4:
                                'mul', 5: 'imul', 6: 'div', 7: 'idiv' }], 
    0xFF : [ None, True, 'm', { 0: 'inc', 1: 'dec', 2: 'call', 3: 'call', 4:
                                'jmp', 5: 'jmp', 6: 'push' }],
    #0x0F 0xAE : [ None , True, 'm', { 0: 'fxsave', 1: 'fxrstor', 2: 'ldmxcsr', 3: 'stmxcsr', 4: 'xsave', 5: 'xrstor', 6: 'xsaveopt', 7: 'clflush' } ],
}

GLOBAL_REGISTER_NAMES = [ 'eax', 'ecx', 'edx', 'ebx', 'esp', 'ebp', 'esi', 'edi' ]

def isValidOpcode(opcode):
    if opcode in GLOBAL_OPCODE_MAP.keys():
        return True
    return False

def parseMODRM(modrm):
    #mod = (modrm & 0xC0) >> 6
    #reg = (modrm & 0x38) >> 3
    #rm  = (modrm & 0x07)

    mod = (modrm & 0b11000000) >> 6
    reg = (modrm & 0b00111000) >> 3
    rm  = (modrm & 0b00000111)
    return (mod,reg,rm)

def printDisasm( l ):

    # Good idea to add a "global label" structure...
    # can check to see if "addr" is in it for a branch reference

    for addr in sorted(l):
        print( '%s: %s' % (addr, l[addr]) )

def disassemble(b):

    ## TM
    # I would suggest maintaining an "output" dictionary
    # Your key should be the counter/address [you can use this
    # to print out labels easily]
    # and the value should be your disassembly output (or some
    # other data structure that can represent this..up to you )
    outputList = {}

    i = 0

    while i < len(b):

        implemented = False
        #opcode = ord(b[i])	#If using python2.7
        opcode = b[i]	#current byte to work on
        #instruction_bytes = "%02x" % ord(b[i]) # if using python 2.7
        instruction_bytes = "%02x" % b[i]
        instruction = ''
        orig_index = i
        
        i += 1

        # Hint this is here for a reason, but is this the only spot
        # such a check is required in?
        if i > len(b):
           break

        

        if isValidOpcode( opcode ):
            print ('Found valid opcode')
            if 1:
                li = GLOBAL_OPCODE_MAP[opcode]
                if li[1] == True:
                    print ('REQUIRES MODRM BYTE')
                    #modrm = ord(b[i])
                    modrm = b[i]
                    mnemonic = li[0]


                    instruction_bytes += ' '
                    #instruction_bytes += "%02x" % ord(b[i])
                    instruction_bytes += "%02x" % b[i]

                    i += 1 # we've consumed it now
                    mod,reg,rm = parseMODRM( modrm )

                    if li[0] == None:
                        print('Need to look at the REG field modrm for the opcode extension')
                        mnemonic = 'UPDATEME'

                    if mod == 3:
                        implemented = True
                        print ('r/m32 operand is direct register')
                        instruction += mnemonic
                        if li[2] == 'mr':
                            instruction += GLOBAL_REGISTER_NAMES[rm]
                            instruction += ', '
                            instruction += GLOBAL_REGISTER_NAMES[reg]
                        elif li[2] == 'rm':
                            instruction += GLOBAL_REGISTER_NAMES[reg]
                            instruction += ', '
                            instruction += GLOBAL_REGISTER_NAMES[rm]

                    elif mod == 2:
                        #Uncomment next line when you've implemented this 
                        #implemented = True
                        print ('r/m32 operand is [ reg + disp32 ] -> please implement')
                        # will need to parse the displacement32
                    elif mod == 1:
                        #Uncomment next line when you've implemented this 
                        #implemented = True
                        print ('r/m32 operand is [ reg + disp8 ] -> please implement')
                        # will need to parse the displacement8
                    else:
                        if rm == 5:
                            #Uncomment next line when you've implemented this
                            #implemented = True
                            print ('r/m32 operand is [disp32] -> please implement')
                        elif rm == 4:
                            #Uncomment next line when you've implemented this
                            #implemented = True
                            print ('Indicates SIB byte required -> please implement')
                        else:
                            #Uncomment next line when you've implemented this
                            #implemented = True
                            print ('r/m32 operand is [reg] -> please implement')

                    if implemented == True:
                        print ('Adding to list ' + instruction)
                        outputList[ "%08X" % orig_index ] = instruction_bytes + ' ' + instruction
                    else:
                        outputList[ "%08X" % orig_index ] = 'db %02x' % (int(opcode) & 0xff)
                else:
                    print ('Does not require MODRM - modify to complete the instruction and consume the appropriate bytes')
                    outputList[ "%08X" % orig_index ] = 'db %02x' % (int(opcode) & 0xff)
            #except:
            else:
                outputList[ "%08X" % orig_index ] = 'db %02x' % (int(opcode) & 0xff)
                i = orig_index
        else:
            outputList[ "%08X" % orig_index ] = 'db %02x' % (int(opcode) & 0xff)


    printDisasm (outputList)


def getfile(filename):	
    with open(filename, 'rb') as f:
        a = f.read()
    return a		

def main():
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-e', '--examplearg', help='Shows an example usage', dest='examplename', required=True)
    #args = parser.parse_args()
    
    # access the value using:
    #if args.examplename != None:
    #    print("Passed in value %s" % args.examplename)


    import sys 
    if len(sys.argv) < 2:
        print ("Please enter filename.")
        sys.exit(0)
    else:
        binary = getfile(sys.argv[1])

    disassemble(binary)


if __name__ == '__main__':
    main()

