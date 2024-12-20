from collections import defaultdict, deque
import heapq as heap

WALLS = set()
DOORS  = defaultdict(int)
DDOORS = defaultdict(int)
KEYS   = defaultdict(int)
KKEYS  = defaultdict(int)

start = (0,0)

lines = open('18.in').read().splitlines()

R = len(lines)
C = len(lines[0])
locs = []
grid = []

for r,row in enumerate(lines):
    line = []
    for c,col in enumerate(row):
        line.append(col)
        loc = (r,c)
        if col == '@' : start = loc
        elif ord(col) in range(ord('a'),ord('z')+1):
            KEYS[loc] = col
            KKEYS[col] = loc
        elif ord(col) in range(ord('A'),ord('Z')+1):
            DOORS[loc] = col
            DDOORS[col] = loc
    grid.append(line)

# Draw the current state
def draw_grid():
    global WALLS,DOORS,KEYS,locs
    for r in range(R):
        row = ''
        for c in range(C):
            loc = (r,c)
            if   grid[r][c] == '#': row += '#'
            elif loc == start: row += '@'
            elif loc in locs:  row += '@'
            #elif loc in locs:  row += '@'
            elif loc in KEYS:  row += KEYS[loc]
            elif loc in DOORS: row += DOORS[loc]
            else:              row += '.'
        print(row)

def reachable_keys(loc, keys):
    "Which keys can we get to from here that aren't in the provided keys list?"
    Q = deque()
    Q.append((0, loc))
    SEEN = set()

    while Q:
        steps, loc = Q.popleft()
        if loc in SEEN: continue
        SEEN.add(loc)
        # It's a key but we don't have it yet
        if loc in KEYS and loc not in keys:
            yield steps, loc
            continue
        # Move to the adjacent squares
        r,c = loc
        for dr,dc in [(-1,0),(1,0),(0,1),(0,-1)]:
            nr,nc = r+dr,c+dc
            nloc = (nr,nc)
            if grid[nr][nc] == '#': continue
            # Can't go through a locked door
            if nloc in DOORS and KKEYS[DOORS[nloc].lower()] not in keys: continue
            # Otherwise we can move
            Q.append((steps+1, nloc))

def solve(locs):
    Q = []
    heap.heappush(Q, (0, locs, frozenset()))
    SEEN = set()

    while Q:
        steps, clocs, keys = heap.heappop(Q)
        # If we've got all the keys then that's the minimum route
        if len(KEYS) == len(keys):
            return steps
        # Been here before?
        if (clocs, keys) in SEEN: continue
        SEEN.add((clocs,keys))
        # Try to get to all the other keys
        for i in range(len(clocs)):
            for dsteps, dloc in reachable_keys(clocs[i], keys):
                # Update locs
                dlocs = clocs[:i] + (dloc,) + clocs[i+1:]
                heap.heappush(Q, (steps+dsteps, dlocs, keys | frozenset([dloc]) ) )

locs = []
locs.append(start)
locs = tuple(locs)
min_steps = solve(locs)
print('Part 1:', solve(locs))

# -- Part 2 --

# Update the walls to chop the map into into 4 quadrants

# Original start position becomes a wall
grid[start[0]][start[1]] = '#'

# N, E, S, W of the start position also become walls
for dr,dc in [(-1,0),(1,0),(0,1),(0,-1)]:
    nr,nc = dr+start[0], dc+start[1]
    grid[nr][nc] = '#'

# Start locations for the 4 robots are diagonals one step from the original start
locs = []
for i,(dr,dc) in enumerate([(-1,1),(1,-1),(1,1),(-1,-1)]):
    nr,nc = dr+start[0], dc+start[1]
    locs.append((nr,nc))
locs = tuple(locs)
print('Part 2:', solve(locs))
