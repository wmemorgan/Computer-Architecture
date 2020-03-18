#!/usr/bin/env python3

"""Main."""

import sys
from util import load_to_memory
from cpu import *

cpu = CPU()
# Confirm program file is specified
if len(sys.argv) < 2:
    print("Missing LS8 program file")
    sys.exit(2)
elif len(sys.argv) > 2:
    print("Invalid command line format")
    sys.exit(2)

# Import commands into a program
program = load_to_memory(sys.argv[1])

# Validate program and invoke emulator
if len(program) > 0:
    cpu.load(program)
    cpu.run()

else:
    print("Invalid program loaded")
    sys.exit(1)
            
