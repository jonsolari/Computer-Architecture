"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        
    
    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    line = line.split('#', 1)[0]
                    value = line.rstrip()
                    if value == "":
                        continue
                    num = int(value, 2)
                    self.ram_write(num, address)
                    address += 1
        except FileNotFoundError:
            print("File not found")    
            sys.exit(2)
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        sp = 255
        while True:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            self.reg[7] = sp

            if ir == 0b10000010 or ir == "LDI":
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == 0b01000111 or ir == "PRN":
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == 0b00000001 or ir == "HLT":
                sys.exit(0)
            elif ir == 0b10100000 or ir == "ADD":
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b10100010 or ir == "MUL":
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif ir == 0b01000101 or ir == "PUSH":
                sp -= 1
                self.ram_write(self.reg[operand_a], sp)
                self.pc += 2
            elif ir == 0b01000110 or ir == "POP":
                self.reg[operand_a] = self.ram_read(sp)
                sp +=1
                self.pc += 2
            elif ir == 0b01010000 or ir == "CALL":
                sp -= 1
                self.ram_write(self.pc, sp)
                self.pc = self.reg[operand_a]
            elif ir == 0b00010001 or ir == "RET":
                self.pc = self.ram_read(sp) + 2
                sp += 1
                
                

                

