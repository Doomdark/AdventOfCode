lines = open("06.in").read().splitlines()

import copy

obstructions = set()
start = None

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == '#': obstructions.add((r,c))
        elif char == '^': start = (r,c)

max_r = len(lines)-1
max_c = len(lines[0])-1

# Starting moving direction
direction = (-1,0)

# Right turns. Direction -> next direction
turn_right = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}

# Perform a move
def move(loc,direction,obs):
    r,c = loc
    dr,dc = direction
    nr,nc = r+dr, c+dc
    # If the next square is an obstacle then turn instead of moving
    if (nr,nc) in obs:
        direction = turn_right[direction]
        return (loc, direction)
    else:
        loc = (nr,nc)
        return (loc, direction)

# Solve it!
def solve(start, direction, part2=False, extra=None):
    global obstructions
    loc = start
    d = direction
    visited = set()
    loop = False
    obs = None

    # Add the extra obstruction for part 2
    if part2:
        obs = copy.copy(obstructions)
        obs.add(extra)
    else:
        obs = obstructions

    while (True):
        # Store the direction in the visited set for part 2 as that indicates if we're in a loop
        if part2:
            visited.add((loc, d))
        else:
            visited.add(loc)
        # Move
        nloc, ndir = move(loc, d, obs)
        nr,nc = nloc
        # Outside the grid?
        if nr < 0 or nr > max_r or nc < 0 or nc > max_c:
            break
        elif part2:
            # Check if the next location/direction has been visited before
            id = (nloc, ndir)
            if id in visited:
                loop = True
                break
        # Next location
        loc = nloc
        d = ndir

    return loop if part2 else visited

part1 = solve(start, direction)
print('Part 1:', len(part1))

# For each location visited in part1 add an obstruction and solve to see if we're in a loop

loop_count = 0
for r,c in part1:
    # Don't add a new obstruction in an existing location
    if (r,c) == start:
        continue
    direction = (-1,0)
    loop_count += solve(start, direction, part2=True, extra=(r,c))

print('Part 2:', loop_count)
