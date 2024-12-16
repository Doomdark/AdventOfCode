import heapq as heap
import copy

lines = open('16.in').read().splitlines()

R = len(lines)
C = len(lines[0])

S = None
E = None
walls = set()

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if char == '#': walls.add((r,c))
        elif char == 'S': S = (r,c)
        elif char == 'E': E = (r,c)

def print_grid(path):
    for r in range(R):
        l = ''
        for c in range(C):
            if   (r,c) in walls: l += '#'
            elif (r,c) in path:  l += '@'
            else: l += '.'
        print(l)

Q = []
heap.heappush(Q, (S,0,set(),(1,0),[])) # Start facing east
min_cost = None
min_path = None

while Q:
    #print(len(Q))
    loc,cost,SEEN,ldir,path = heap.heappop(Q)
    npath = path + [loc]
    if loc == E:
        if min_cost is None or cost < min_cost:
            min_cost = cost
            min_path = npath
            print(min_cost)
        continue
    if min_cost is not None and cost >= min_cost:
        continue
    # Been here before
    if loc in SEEN: continue
    _SEEN = copy.copy(SEEN)
    _SEEN.add(loc)
    r,c = loc
    # Try to go in every direction
    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr,nc = r+dr,c+dc
        if (nr,nc) not in walls and (nr,nc) not in SEEN:
            # Cost is +1000 if we didn't go in the same direction as last time
            cost_add = 1 if ldir == (dr,dc) else 1001
            ncost = cost_add+cost
            heap.heappush(Q, ((nr,nc),ncost,_SEEN,(dr,dc),npath))

#print_grid(min_path)

print('Part 1:', min_cost)
