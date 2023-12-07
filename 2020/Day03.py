from collections import deque
import numpy, copy

rows = []

with open("Day03_input.txt") as f:
    for line in f.readlines():
        r = deque()
        for char in line.rstrip():
            r.append(char)
        rows.append(r)

def traverse(right, down):
    _rows = copy.deepcopy(rows)
    crash = 0
    row = 0
    # Iterate for the number of rows
    for n in range(len(rows)-1):
        # Rotate the rows first
        for r in _rows:
            r.rotate(right*-1)
        # Next row
        row += down
        if row >= len(rows):
            return crash
        if _rows[row][0] == '#':
            crash += 1

    return crash

print "Part 1:", traverse(3, 1)

traverses = []
traverses.append(traverse(1, 1))
traverses.append(traverse(3, 1))
traverses.append(traverse(5, 1))
traverses.append(traverse(7, 1))
traverses.append(traverse(1, 2))

print "Part 2:", numpy.prod(traverses)
