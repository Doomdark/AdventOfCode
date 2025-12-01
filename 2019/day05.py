from intcode import Intcode
from collections import defaultdict

program = defaultdict(int)
line = open('day05_input.txt').read().strip()
for i,code in enumerate([int(x) for x in line.split(',')]):
    program[i] = code

# Part 1 - input 1
d = Intcode(program)
d.put(1)
d.run()
while True:
    o = d.get()
    if o == 0:
        continue
    else:
        print("Part 1:", o)
        break

# Reinitialise the program

# Part 2 - input 5
d = Intcode(program)
d.put(5)
d.run()
print("Part 2:", d.get())
