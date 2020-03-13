"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # Memory (RAM)
        self.ram = [0] * 256
        # Registers
        self.reg = [0] * 8
        # Program Counter
        self.pc = 0
        # Stack pointer
        self.sp = self.reg[7]
        # CPU status
        self.running = False

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        return self.ram[mar]

    def load(self, program):
        """Load a program into memory."""

        address = 0
        print(f"load program into memory: {program}")

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

        self.running = True
        while self.running:
            # It needs to read the memory address that's stored in register `PC`
            # store that result in `IR`
            ir = self.ram[self.pc]
            opcode = ir

            if opcode == 1:
                self.halt()

            elif opcode == 130:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.ldi(operand_a, operand_b)

            elif opcode == 71:
                operand_a = self.ram_read(self.pc + 1)
                self.prn(operand_a)

            else:
                self.pc += 1


    def halt(self):
        """Halt CPU (exit emulator)."""

        print("Halt program. Exit emulator.")
        self.running = False
        sys.exit()


    def ldi(self, address, value):
        """Set the value of a register to an inter"""

        self.reg[address] = value
        print(f"Set {value} to R{address}")
        self.pc += 3


    def prn(self, address):
        """Print numeric value stored in the given register"""

        print(f"{self.reg[address]} in R{address}")
        self.pc += 2
