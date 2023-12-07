import sys
sys.path.append('/home/rwilkinson/Python')

from intcode import Intcode
from collections import defaultdict

# Program memory
program = defaultdict(int)

# Read the intcode program
with open("day17_input.txt",'r') as f:
    for line in f.readlines():
        for i,x in enumerate(line.rstrip().split(',')):
            program[i] = int(x)

# Run the computer
c = Intcode(program)
c.start()

while True:
    a = c.get()
    if a is not None:
        print chr(a),
    else:
        break
