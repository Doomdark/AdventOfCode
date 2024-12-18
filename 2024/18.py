import heapq
from collections import defaultdict

lines = open('18.in').read().splitlines()

# Read all the bytes
bytes = []
for line in lines:
    x,y = line.split(',')
    bytes.append((int(x),int(y)))

X,Y = 70,70
walls = set()

# Let N bytes fall
for i in range(1024):
    walls.add(bytes[i])

def solve(WALLS):
    # Find the shortest path to the exit
    Q = []
    SEEN = defaultdict(lambda:10**9)
    heapq.heappush(Q, (0, (0,0)) )

    while Q:
        dist, loc = heapq.heappop(Q)
        # Reached the end first? That's the shortest distance.
        if loc == (X,Y):
            return dist
        # Took same/longer to get here than before?
        if dist >= SEEN[loc]:
            continue
        # New distance for this location
        SEEN[loc] = dist
        x,y = loc
        # Try to go in all directions
        for dx,dy in [(-1,0), (0,-1), (1,0), (0,1)]:
            # Next location to visit
            nx,ny = x+dx,y+dy
            # On the grid and not a wall?
            if 0<=nx<=X and 0<=ny<=Y and (nx,ny) not in WALLS:
                heapq.heappush(Q, (dist+1, (nx,ny)) )
    return None

print('Part 1:', solve(walls))

# -- Part 2 --

# Work backwards. Add all the bytes initially and check for a path.
# The more bytes there are the fewer paths there will be to check.
# Then run again with one fewer bytes.
# Find the first solution where there is a valid path then the answer is the previous byte.
import copy
walls_orig = copy.copy(walls)

# Add all the bytes until the decreasing end value
for end in range(len(bytes),1024,-1):
    walls = copy.copy(walls_orig)
    # Add the rest of the bytes
    for i in range(1024, end):
        walls.add(bytes[i])
    if solve(walls):
        print('Part 2: {},{}'.format(bytes[end][0], bytes[end][1]))
        exit()
