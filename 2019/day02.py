import copy,sys

initial_program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,5,19,23,2,9,23,27,1,6,27,31,1,31,9,35,2,35,10,39,1,5,39,43,2,43,9,47,1,5,47,51,1,51,5,55,1,55,9,59,2,59,13,63,1,63,9,67,1,9,67,71,2,71,10,75,1,75,6,79,2,10,79,83,1,5,83,87,2,87,10,91,1,91,5,95,1,6,95,99,2,99,13,103,1,103,6,107,1,107,5,111,2,6,111,115,1,115,13,119,1,119,2,123,1,5,123,0,99,2,0,14,0]

program = copy.deepcopy(initial_program)

def run():
    # Start program at address 0
    addr = 0

    while 1:
        opcode = program[addr+0]
        param1 = program[addr+1]
        param2 = program[addr+2]
        param3 = program[addr+3]

        if opcode == 1:
            program[param3] = program[param1] + program[param2]
            addr += 4
        elif opcode == 2:
            program[param3] = program[param1] * program[param2]
            addr += 4
        elif opcode == 99:
            return program[0]
        else:
            print("Unknown opcode at addr", addr)

# Part 1
noun = 12
verb = 2

# Replace program entries 1 and 2 as directed
program[1] = noun
program[2] = verb

print("Part 1:", run())

# Part 2
for noun in range(0,100):
    for verb in range(0,100):
        # Re-initialise the program
        program = copy.deepcopy(initial_program)
        # Replace program entries 1 and 2 as directed
        program[1] = noun
        program[2] = verb
        # Run the program
        if run() == 19690720:
            print("Part 2: 100 * noun + verb =", 100 * noun + verb)
            sys.exit()
