from collections import defaultdict, deque
import heapq as heap

lines = open('10.in').read().splitlines()

def dijkstra(G, startingNode):
    visited = set()
    parentsMap = {}
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    heap.heappush(pq, (0, startingNode))
    
    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heap.heappop(pq)
        visited.add(node)

        for adjNode, weight in G[node].items():
            if adjNode in visited:  continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                parentsMap[adjNode] = node
                nodeCosts[adjNode] = newCost
                heap.heappush(pq, (newCost, adjNode))

    return parentsMap, nodeCosts

Graph = defaultdict(dict)
Grid  = defaultdict()

max_r = 0
max_c = 0

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        Grid[(r,c)] = char
        if char == '.':
            continue
        # Figure out how the S square connects after we've done the rest of the graph
        if char == 'S':
            start = (r,c)
            continue
        # Work out the connectivity
        if   char == '-': adjacents = [(0,-1),(0,1)]
        elif char == 'F': adjacents = [(1,0),(0,1)]
        elif char == '|': adjacents = [(1,0),(-1,0)]
        elif char == 'L': adjacents = [(0,1),(-1,0)]
        elif char == 'J': adjacents = [(0,-1),(-1,0)]
        elif char == '7': adjacents = [(0,-1),(1,0)]
        for dr,dc in adjacents:
            nr,nc=r+dr,c+dc
            Graph[(r,c)][(nr,nc)] = 1
        max_c = max(c,max_c)
    max_r = max(r,max_r)

# Now determine what type of square S is
n,e,s,w=0,0,0,0

# Shove in all the try statements to make it ignore off-grid errors
nr,nc=start[0]+0,start[1]+1
try:
    if Grid[(nr,nc)] in ['-', 'J', '7']:
        Graph[start][(nr,nc)] = 1
        e=1
except:
    pass
nr,nc=start[0]+0,start[1]-1
try:
    if Grid[(nr,nc)] in ['-', 'L', 'F']:
        Graph[start][(nr,nc)] = 1
        w=1
except:
    pass
nr,nc=start[0]+1,start[1]+0
try:
    if Grid[(nr,nc)] in ['|', 'J', 'L']:
        Graph[start][(nr,nc)] = 1
        s=1
except:
    pass
nr,nc=start[0]-1,start[1]+0
try:
    if Grid[(nr,nc)] in ['|', 'F', '7']:
        Graph[start][(nr,nc)] = 1
        n=1
except:
    pass

# What type of square is S?
if   n and e: Grid[start] = 'L'
elif s and e: Grid[start] = 'F'
elif n and w: Grid[start] = 'J'
elif s and w: Grid[start] = '7'
elif n and s: Grid[start] = '|'
elif e and w: Grid[start] = '-'

# Solve part 1
parentsMap, nodeCosts = dijkstra(Graph, start)
print('Part 1:', max([x for x in nodeCosts.values()]))

# Part 2

# Traverse round the loop and mark which locations the main loop resides.

dirs = {'n':(-1,0), 'e':(0,1), 's':(1,0), 'w':(0,-1)}

loop = set()
loop.add(start)

loc = start
moving = None

done = False
while not done:
    # Go in one of the directions from S
    r,c = loc
    # Not started moving yet
    if loc == start:
        if   Grid[loc] in ['-', 'F', 'L'] : moving = 'e'
        elif Grid[loc] in ['|', '7']      : moving = 's'
        elif Grid[loc] in ['J']           : moving = 'n'
    else: # Already moving
        if Grid[loc] == 'F':
            if   moving == 'n': moving = 'e'
            elif moving == 'w': moving = 's'
        elif Grid[loc] == '7':
            if   moving == 'n': moving = 'w'
            elif moving == 'e': moving = 's'
        elif Grid[loc] == 'J':
            if   moving == 's': moving = 'w'
            elif moving == 'e': moving = 'n'
        elif Grid[loc] == 'L':
            if   moving == 's': moving = 'e'
            elif moving == 'w': moving = 'n'

    # Get the movement for the next location
    dr,dc = dirs[moving]

    # New location along the pipe
    loc = (r+dr,c+dc)
    
    # Back at the start of the loop
    if loc == start:
        done = True

    # Add this location to the loop
    loop.add(loc)

inside_count = 0

# Keep track of the number of pipe traversals and junction crossings for each row.
for r in range(max_r):
    # Keep track of if we're inside on this row
    inside = 0
    # Stack of matches for pipe corners
    lasts = deque()
    # Traverse the row
    for c in range(max_c):
        # Current location
        loc = (r,c)
        # Character in this grid location
        v = Grid[(r,c)]
        # Is the location on the main loop?
        if not loc in loop:
            if inside > 0:
                inside_count += 1
            continue
        
        # If we're not inside the loop then see if we are about to be
        if inside:
            if v == '|':
                inside -= 1
            elif v in 'FL':
                lasts.append(v)
            elif v in 'J' and lasts[-1] in 'F':
                inside -= 1
                lasts.pop()
            elif v in '7' and lasts[-1] in 'L':
                inside -= 1
                lasts.pop()
        else:
            if v == '|':
                inside += 1
            elif v in 'FL':
                lasts.append(v)
            elif v in 'J' and lasts[-1] in 'F':
                inside += 1
                lasts.pop()
            elif v in '7' and lasts[-1] in 'L':
                inside += 1
                lasts.pop()
                    
print('Part 2:', inside_count)

