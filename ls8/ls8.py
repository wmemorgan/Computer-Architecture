#!/usr/bin/env python3

"""Main."""

import sys
from util import lines_to_program
from cpu import *

cpu = CPU()
# Confirm input file exists
if len(sys.argv) <= 1:
    print("Missing input file.")
    cpu.halt()

# Read file
f = open(sys.argv[1], "r")
lines = f.readlines()
f.close()

# Import commands into a program
program = lines_to_program(lines)

# Validate program and invoke emulator
if program is not None or len(program) > 0:
    cpu.load(program)
    cpu.run()

else:
    print("Invalid program")
    cpu.halt()
            
