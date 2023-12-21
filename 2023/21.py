from collections import deque, defaultdict
from heapq import heappush, heappop
import math

def dijkstra(G, startingNode):
    visited = set()
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    heappush(pq, (0, startingNode))

    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node = heappop(pq)
        visited.add(node)

        for adjNode, weight in G[node].items():
            if adjNode in visited:  continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                nodeCosts[adjNode] = newCost
                heappush(pq, (newCost, adjNode))

    return nodeCosts

lines = open('21.in').read().splitlines()

walls = set()
start = None

max_r, max_c = 0,0

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == 'S': start = (r,c)
        elif char == '#': walls.add((r,c))
        max_c = max(max_c,c)
    max_r = max(max_r,r)

size_r = max_r+1
size_c = max_c+1

def get_moves(loc):
    l = []
    r,c = loc
    for dr,dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        nr,nc = (r+dr,c+dc)
        if 0<=nr<=max_r and 0<=nc<=max_c and (nr,nc) not in walls:
            l.append((nr,nc))
    return l

# Make a graph of the grid
G = defaultdict(dict)
for r in range(max_r+1):
    for c in range(max_c+1):
        loc = (r,c)
        for nloc in get_moves(loc):
            G[loc][nloc] = 1

def solve(turns=6):
    global start
    endpoints = set()
    # Get all the node costs
    nodeCosts = dijkstra(G, start)
    # Check each location
    for r in range(max_r+1):
        for c in range(max_c+1):
            loc = (r,c)
            # Get the shortest distance from start to each point
            # If it's divisible by 2 then you can get there
            length = nodeCosts[loc]
            if length <= turns and length %2 == 0:
                endpoints.add(loc)
    return len(endpoints)

print('Part 1:', solve(64))

# Part 2

# The input data has a clear channel in a cross from S going W->E and N->S.
# Plus it has clear edges, so you can get to each corner and each edge with the Manhattan distance.

grid = lines

# Get possible neighbours accommodating locations which are larger than the grid size
def get_neighbors(grid, loc):
    r,c = loc
    for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        nr, nc = r+dr, c+dc
        nloc = (nr, nc)
        # If the grid isn't a wall then it's valid
        if grid[nr % size_r][nc % size_c] != '#':
            yield nloc

# Find the total number of destination squares for a given grid size
def bfs(grid, src, maxdist, get_neighbors=None):
    queue = deque()
    queue.append((0,src))
    visited = set()
    total = 0
    # Get the parity of the max distance. The grid is an odd width/height so the parity changes on alternate cells.
    parity = maxdist % 2
    
    while queue:
    	dist, loc = queue.popleft()
        # Gone too far so break out of the loop
    	if dist > maxdist: break
        # Been here
    	if loc in visited: continue
        # Destination square
    	if dist % 2 == parity: total += 1
        # Add that we've been here
    	visited.add(loc)
        # Get all the possible destinations and add them to the queue
    	for nloc in get_neighbors(grid, loc):
            # If we've not already visited that is
            if nloc not in visited:
    	        queue.append((dist+1, nloc))
    
    return total

# Steps that the elf is taking
total_steps = 26501365
# Number of extra steps after repeats
extra = total_steps % size_r

# Get the first, second and third set of totals for the quadratic sequence
a = bfs(grid, start, extra,                   get_neighbors)
b = bfs(grid, start, extra + size_r,          get_neighbors)
c = bfs(grid, start, extra + size_r + size_r, get_neighbors)

# Diffs are:
# a              b              c
#    1st diff 1     1st diff 2
#            2nd diff

# Differences between successive iterations. Day 9 was sort of similar.
first_diff1 = b - a
first_diff2 = c - b
second_diff = first_diff2 - first_diff1

# https://www.radfordmathematics.com/algebra/sequences-series/difference-method-sequences/quadratic-sequences.html
A = second_diff//2
B = first_diff1 - 3*A
C = a - B - A

def quadratic_sequence(n, a, b, c):
    return a*n**2 + b*n + c

repeats = math.ceil(total_steps/size_r)
answer = quadratic_sequence(repeats, A, B, C)

print('Part 2:', answer)
