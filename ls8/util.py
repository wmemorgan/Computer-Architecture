# Convert file output to program code
def lines_to_program(lines):
    # Confirm file output is not empty
    if len(lines) == 0:
        print("Empty input file")
        return None

    program = []
    for line in lines:
        if line[0] == '0' or line[0] == '1':
            program.append(int(line[:8], 2))

    return program
