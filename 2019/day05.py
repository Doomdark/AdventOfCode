import copy
from intcode import Intcode

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

# Part 1 - input 1
print("Part 1:")
d = Intcode(program)
d.input_value = 1
d.run()
print(d.get())

# Reinitialise the program

# Part 2 - input 5
print("Part 2:")
d = Intcode(program)
d.input_value = 5
d.run()
print(d.get())
