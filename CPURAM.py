#DEFINES FUNCTIONALITY OF THE 6510 CPU and RAM

###imports
import time
import numpy as np
import pandas as pd

### data, runtime variables and directories

decoder_data = 'C:/Users/lucco/Desktop/emulator project/6502ops.csv'
### useful functions

def truncate_to_byte(val): #keeps the 8 least most significant digits in a chunk of binary data
    truncated = val%256
    return truncated

def truncate_to_64K(val): #keeps most signficant 16 bits of address in case longer-than-expected address is suppliued
    truncated = val%(2**16)
    return truncated

### component classes

class Memory(): #RAM

    def __init__(self, size = (2**16), def_val = 0): #creates a chunk of contiguous memory
        self.mem = np.full((1,size), def_val)
        self.last_valr = ''
        self.last_valw = ''
        self.last_addr = ''

    def read(self, address): #reads byte of memory from supplied address
        address = truncate_to_64K(address)
        #fetching data at address
        read_value = self.mem[0,address]
        #saving telemetry about access
        self.last_valr = read_value
        self.last_addr = address

        return read_value

    def write(self, address, data): #writes byte of memory to supplied address
        address = truncate_to_64K(address) #sanity check
        data = truncate_to_byte(data) #sanity check for data to make sure we're not writing more than 8bits
        #memory write
        self.mem[0,address] = data
        #updating telemetry
        self.last_valw = data
        self.last_addr = address

    def flush(self, def_val = 0): #clears all memory
        #iterate through array
        for j in self.mem:
            for i in j:
                self.mem[j,i] = def_val
        #telemtry
        self.last_addr = ''
        self.last_valr = ''
        self.last_valw = def_val

class Decoder():

    def __init__(self, dec_dir): #loads decoder data from csv file
        self.dec_matrix = pd.read_csv(decoder_data)

    def decode(self, opcode): #return info on opcode being supplied
        #checking types
        if type(opcode) == str:
            opcode = opcode
        if type(opcode) == int:
            opcode = hex(opcode)
        #extract opcode and other data
        row = self.dec_matrix.loc[self.dec_matrix['opcode'] == opcode]
        if row.empty == True: #ERROR INVALID OPCODE
            raise Exception("ERROR: Invalid/Unrecognized Opcode")
        #flag check
        flags = row.core_flags.item()

        #extract data
        self.last_opcode = row.opcode.item()
        self.last_mnemonic = row.mnemonic.item()
        self.last_addrmode = row.addressing.item()
        self.last_instr_size = row.bytes.item()
        self.last_instr_latency = int(row.cycles.item())
        self.last_instr_flags = row.core_flags.item()
        return self.last_opcode



class CPU_registers():
    def __init__(self):
        #registers
        self.A = 0
        self.X = 0
        self.Y = 0
        self.PC = 0
        self.SP = 0
        self.SR = {'N' : 0, 'V' : 0, 'B' : 0, 'D' : 0, 'I' : 0, 'Z' : 0, 'C' : 0}

class Processor():

    def __init__(self):
        self.model = 'MOS6502'
        self.revision = 'rev 0.01'
        self.functionality = 'none'
        #current step in current operation
        self.step = 0

    def cycle(self, registers, memory, decoder): #clock tick: do the next task
    #if currently NOT doing something, grab opcode at current address
        if self.step == 0: #new operation
            curr_opcode = memory.read(registers.PC)
            #print(curr_opcode)
            print(registers.PC)
            registers.PC += 1

class Clock():

    def __init__(self, frequency):
         self.frequency = frequency
         self.period = 1/self.frequency
    def tick(self, cpu, registers, memory, decoder):
        time.sleep(self.period) #TEMPORARY, NOT ACCURATE TIMER
        cpu.cycle(registers, memory, decoder)

ram = Memory()
reg = CPU_registers()
dec = Decoder(decoder_data)
cpu = Processor()
clk = Clock(10000)
while(1):
    clk.tick(cpu, reg,ram,dec)









