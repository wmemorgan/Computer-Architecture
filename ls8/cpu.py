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
        self.reg[7] = 0xF4
        # CPU status
        self.running = False
        # Branch table
        self.branchtable = {}
        self.branchtable['HLT'] = self.halt
        self.branchtable['LDI'] = self.ldi
        self.branchtable['PRN'] = self.prn
        self.branchtable['PUS'] = self.push
        self.branchtable['POP'] = self.pop
        self.branchtable['CAL'] = self.call
        self.branchtable['RET'] = self.ret

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        return self.ram[mar]

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            print(f"Multiply {self.reg[reg_a]} by {self.reg[reg_b]}")
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        # print(f"TRACE: %02X | %02X %02X %02X |" % (
        #     self.pc,
        #     # self.fl,
        #     # self.ie,
        #     self.ram_read(self.pc),
        #     self.ram_read(self.pc + 1),
        #     self.ram_read(self.pc + 2)
        # ), end='')
        print(
            f"TRACE: {self.pc} | {self.ram_read(self.pc)} {self.ram_read(self.pc + 1)} {self.ram_read(self.pc + 2)} |")

        for i in range(8):
            # print(" %02X" % self.reg[i], end='')
            print(f"R[{i}] is {self.reg[i]}")

        print()

    def halt(self):
        """Halt CPU (exit emulator)."""

        print("Halt program. Exit emulator.")
        self.running = False
        sys.exit()

    def ldi(self, address, value, nbr_of_args):
        """Set the value of a register to an interger"""

        self.pc += 1
        self.reg[address] = value
        print(f"Set {value} to R{address}")
        self.pc += nbr_of_args

    def prn(self, address, nbr_of_args):
        """Print numeric value stored in the given register"""

        self.pc += 1
        print(f"{self.reg[address]} in R{address}")
        self.pc += nbr_of_args

    def push(self, address, nbr_of_args):
        # Decrement the stack pointer
        self.reg[7] -= 1
        # Copy the value from the given register
        value = self.reg[address]
        # Save the register value to the top of the stack
        self.ram[self.reg[7]] = value
        # Increment program counter
        self.pc += nbr_of_args + 1

    def pop(self, address, nbr_of_args):
        # Copy the value from the address pointed to by the
        # stack pointer to the given register
        value = self.ram[self.reg[7]]
        self.reg[address] = value
        # Increment the stack pointer
        self.reg[7] += 1
        # Increment program counter
        self.pc += nbr_of_args + 1

    def call(self, address, nbr_of_args):
        self.pc += 1
        # Decrement the stack pointer
        self.reg[7] -= 1
        # Save the next instruction address to the top of the stack
        self.ram[self.reg[7]] = self.pc + nbr_of_args
        # Set the pc to the address stored in the given register
        self.pc = self.reg[address]

    def ret(self):
        # Pop the value from the top of the stack and store it in PC
        self.pc = self.ram[self.reg[7]]
        # Increment stack pointer
        self.reg[7] += 1

    def run(self):
        """Run the CPU."""

        self.running = True
        while self.running:
            if self.ram[self.pc].find('#') != -1:
                ir = self.ram[self.pc].split('#')
                # Extract and parse machine code
                opcode = ir[0]
                op = ir[1][1:4]

                # Define arguments
                nbr_of_args = int(opcode, 2) >> 6

                # Invoke function from branch table based on number of arguments
                if nbr_of_args == 0:
                    self.branchtable[op]()

                elif nbr_of_args == 1:
                    operand_a = int(self.ram_read(self.pc + 1), 2)
                    self.branchtable[op](operand_a, nbr_of_args)

                elif nbr_of_args == 2:
                    operand_a = int(self.ram_read(self.pc + 1), 2)
                    operand_b = int(self.ram_read(self.pc + 2), 2)

                    # Check if arithmetic function
                    is_alu = bool(int(opcode) >> 5 & 0b00000001)
                    if is_alu:
                        self.pc += 1
                        self.alu(op, operand_a, operand_b)
                        self.pc += nbr_of_args

                    else:
                        self.branchtable[op](operand_a, operand_b, nbr_of_args)

                else:
                    # Increment program counter
                    self.pc += 1

            else:
                print(f"No machine instructions")
                self.halt()
