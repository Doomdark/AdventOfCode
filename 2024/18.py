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
    SEEN = defaultdict()
    DIST = None
    heapq.heappush(Q, (0, (0,0)) )

    while Q:
        dist, loc = heapq.heappop(Q)
        # Reached the end?
        if loc == (X,Y):
            # If the distance travelled is shorter then update DIST
            if DIST is None or dist < DIST:
                DIST = dist
        # Already taken longer to get here than the current minimum
        if DIST is not None and dist > DIST:
            continue
        # Been here before?
        if loc in SEEN:
            # Took same/longer to get here than before?
            if dist >= SEEN[loc]:
                continue
        # New location
        SEEN[loc] = dist
        x,y = loc
        # Try to go in all directions
        for dx,dy in [(-1,0), (0,-1), (1,0), (0,1)]:
            # Next location to visit
            nx,ny = x+dx,y+dy
            # On the grid and not a wall?
            if 0<=nx<=X and 0<=ny<=Y and (nx,ny) not in WALLS:
                heapq.heappush(Q, (dist+1, (nx,ny)) )
    return DIST

print('Part 1:', solve(walls))

# Keep letting bytes fall and just run the solver until it finds the answer. Takes just over 9 seconds on my Mac Mini.
for i in range(1024, len(bytes)):
    walls.add(bytes[i])
    if solve(walls) == None:
        print('Part 2: {},{}'.format(bytes[i][0], bytes[i][1]))
        exit()
