import intcode, copy

program = []
for i in range(10000):
    program.append(0)

# Read in the program
with open("day05_input.txt","r") as f:
    j = 0
    for line in f.readlines():
        for i in line.split(','):
            program[j] = int(i)
            j += 1

source = copy.deepcopy(program)

# Part 1 - input 1
print "Part 1:"
intcode.run(source, 1)

# Reinitialise the program

source = copy.deepcopy(program)

# Part 2 - input 5
print "Part 2:"
intcode.run(source, 5)
