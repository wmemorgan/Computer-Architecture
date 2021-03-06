import sys

# Convert file input to machine code
def load_to_memory(filename):
    program = []
    try:
        f = open(filename)
        for line in f:
            # Extract machine code
            if line[0] == '0' or line[0] == '1':
                program.append(int(line[:8],2))

    except FileNotFoundError:
        print("ERROR: File not found. Please enter valid filename.")
        sys.exit(2)

    return program
