import math

# Read the input
lines = open("06.in").read().splitlines()

grid = []

# Make a grid of all of the numbers
for line in lines:
    if not '+' in line:
        grid.append([int(x) for x in line.split()])
    else:
        grid.append([x for x in line.split()])

R = len(grid)
C = len(grid[0])

total = 0

# Do each column in the number grid
for c in range(C):
    result = 0
    op = grid[-1][c]
    values = [grid[r][c] for r in range(R-1)]
    if op == '+': result = sum(values)
    else:         result = math.prod(values)
    total += result

print('Part 1:', total)

# Part 2 requires each character column to be summed

total = 0
op = None
values = []

# The number of columns is now the number of characters in each line
C = len(lines[0])

# Do each column in the original lines list
for c in range(C):
    result = 0
    # Update the operator if there's a new one
    _op = lines[-1][c]
    if _op != ' ':
        op = _op
    # Get the characters for each column if they aren't a space
    chars = [lines[r][c] for r in range(R-1) if lines[r][c] != ' ']
    # If there are some characters then join them together and make a number and add to the numbers list.
    if chars:
        value = int(''.join(chars))
        values.append(value)
    else: # No characters so we should do the sum now
        if op == '+': result = sum(values)
        else:         result = math.prod(values)
        total += result
        # Clear the values list
        values = []

# Do the final iteration as there's no spare empty column at the end for the loop above
if   op == '+': result = sum(values)
elif op == '*': result = math.prod(values)
total += result

print('Part 2:', total)
