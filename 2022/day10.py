x = 1
pc = 0

insts = open("10.in").read().splitlines()

strengths = []
checks = [20,60,100,140,180,220]

# Pending instruction store
pending = None

## Part 2 ##
rows = []
row = None

for cycle in range(0,240):
    ## Part 1 ##
    if cycle in checks:
        strengths.append(cycle*x)

    # Part 2: Add sprite position before execution
    c = cycle%40
    # First column - initialise the row
    if c == 0:
        row = []
    # Is the cycle number inside the sprite range then draw a lit pixel
    if c in range(x-1,x+2):
        row.append('#')
    else: # Otherwise it's dark
        row.append(' ')
    # If we're on the last column then store the current row
    if c == 39:
        rows.append(row)

    # Do the next instruction
    if pending is None:
        i = insts[pc].split()
        ii = i[0]
        if ii == 'noop':
            # Do nothing
            pending = None
        elif ii == 'addx':
            v = int(i[1])
            pending = (ii,v)
        # Move on to the next instruction
        pc += 1
    else: # Got an instruction to do
        ii,vv = pending
        if ii == "addx":
            nx = x + v
            x = nx
        # No pending instruction now
        pending = None


print("Part 1:", sum(strengths))

## Part 2 ##

print("Part 2:")
for row in range(len(rows)):
    print(''.join(rows[row]))
