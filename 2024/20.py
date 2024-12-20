import heapq

grid = open('20.in').read().splitlines()

R = len(grid)
C = len(grid[0])

S = None

for r,line in enumerate(grid):
    for c,char in enumerate(line):
        if char == 'S': S = (r,c)

DISTANCES = {}

# Make a list of all the location distances from the start of the track
Q = []
heapq.heappush(Q, (0, S))
while Q:
    dist, loc = heapq.heappop(Q)
    # Been here before?
    if loc in DISTANCES: continue
    DISTANCES[loc] = dist
    r,c = loc
    for dr,dc in [(-1,0), (0,-1), (1,0), (0,1)]:
        # Next location to visit
        nr,nc = r+dr,c+dc
        # On the grid and not a wall
        if 0<=nr<R and 0<=nc<C and grid[nr][nc] != '#':
            heapq.heappush(Q, (dist+1, (nr,nc)))

def md(a,b):
    'Manhattan distance'
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

def get_cheat_paths(loc, CHEAT_TIME):
    '''Return a set of path pairs where the difference in distance of
    the on-track paths vs Manhattan distance between the points is >=100.'''
    ans = set()

    # Check each row
    for r in range(1,R-1):
        # Already too far away in rows?
        if abs(r-loc[0]) > CHEAT_TIME: continue
        # Iterate over the columns
        for c in range(1,C-1):
            # Already too far away in columns?
            if abs(c-loc[1]) > CHEAT_TIME: continue
            # Skip walls
            if grid[r][c] == '#': continue
            # Other location to test against
            oloc = (r,c)
            # Skip identical locations
            if loc == oloc: continue
            # Manhattan distance between the two points
            direct = md(loc,oloc)
            # Is the Manhattan distance too far?
            if direct > CHEAT_TIME: continue
            # Ignore paths that are not going to be a forward shortcut
            if DISTANCES[oloc] < DISTANCES[loc]: continue
            # Normal distance between the two points if you take the track
            normal_dist = DISTANCES[oloc] - DISTANCES[loc]
            # Is the difference in the paths GEq 100?
            if normal_dist - direct >= 100:
                ans.add((loc,oloc))
    return ans

for part,cheat_time in [(1,2),(2,20)]:
    cheats = set()
    for r in range(1,R-1):
        for c in range(1,C-1):
            # Don't check walls
            if grid[r][c] == '#': continue
            cheats.update( get_cheat_paths((r,c), cheat_time) )

    print(f'Part {part}:', len(cheats))
