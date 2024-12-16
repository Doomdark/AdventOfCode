import copy
from collections import defaultdict
import heapq

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
            elif (r,c) in path:  l += 'O'
            else: l += '.'
        print(l)

def solve(start, end, start_dir=(1,0), reverse=False):
    Q = []
    if reverse:
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            heapq.heappush(Q, (start,0,set(),(dr,dc),[]) )
    else:
        heapq.heappush(Q, (start,0,set(),start_dir,[]) )

    min_cost = None
    nodes = defaultdict()
    best_paths = defaultdict()
    
    while Q:
        loc,cost,SEEN,ldir,path = heapq.heappop(Q)
        # Accumulate the path
        npath = path + [loc]
        # Reached the end of the line. Well it's allllllllright... ridin' around in the breeze...
        if loc == end:
            # If the cost is lower than the current min cost then that's the best path
            if min_cost is None or cost <= min_cost:
                if cost not in best_paths.keys():
                    best_paths[cost] = set()
                best_paths[cost] |= set(npath)
                min_cost = cost
                print(min_cost)
            continue
        # Been here before?
        if loc in SEEN: continue
        # Nope
        _SEEN = copy.copy(SEEN)
        _SEEN.add(loc)
        # If the path cost is already higher than the min cost then this path is bogus
        if min_cost is not None and cost >= min_cost:
            continue
        # Add a cost to the current node including direction
        if (loc,ldir) in nodes.keys():
            # If the current cost on entering from the same direction is higher than however we got here before then ignore this path
            if cost > nodes[(loc,ldir)]: continue
        nodes[(loc,ldir)] = cost
        r,c = loc
        # Try to go in every direction
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            cost_add = 1
            nr,nc = r+dr,c+dc
            if (nr,nc) not in walls:
                # Cost is +1000 if we didn't go in the same direction as last time
                if ldir != (dr,dc): cost_add += 1000
                ncost = cost_add+cost
                #Q.append( ((nr,nc),ncost,_SEEN,(dr,dc),npath) )
                heapq.heappush(Q, ((nr,nc),ncost,_SEEN,(dr,dc),npath) )

    return min_cost, best_paths, nodes

min_cost, p1_paths, p1_nodes = solve(S,E)
print('Part 1:', min_cost)

#print_grid(best_paths[min_cost])

#_, p2a_paths = solve(E,S,(-1,0))
_, p2b_paths, p2_nodes = solve(E,S,(0,-1), True)

OK = set()
for r in range(R):
    for c in range(C):
        for dir in [(1,0),(-1,0),(0,1),(0,-1)]:
            # (r,c,dir) is on an optimal path if the distance from start to end equals the distance from start to (r,c,dir) plus the distance from (r,c,dir) to end.
            if ((r,c),dir) in p1_nodes and ((r,c),dir) in p2_nodes and p1_nodes[((r,c),dir)] + p2_nodes[((r,c),dir)] == min_cost:
                OK.add((r,c))
print('Part 2:', len(OK))
