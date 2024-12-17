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
        if   char == '#': walls.add((r,c))
        elif char == 'S': S = (r,c)
        elif char == 'E': E = (r,c)

LEFT  = {(-1,0):(0,-1), (0,-1):(1,0), (1,0):(0,1), (0,1):(-1,0)}
RIGHT = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}

def solve(start, end):
    Q = []
    heapq.heappush(Q, (start, 0, set(), (0,1), []) )

    min_cost = None
    best_paths = defaultdict()
    nodes = defaultdict()

    while Q:
        loc, cost, SEEN, dir, path = heapq.heappop(Q)
        # If the path cost is already higher than the min cost then this path is bogus
        if min_cost is not None and cost > min_cost:
            continue
        # Have we reached here before?
        if (loc,dir) in nodes.keys():
            # If the current cost on entering from the same direction is higher than however we got here before then ignore this path
            if cost > nodes[(loc,dir)]: continue
        # Accumulate the path
        newpath = path + [loc]
        # Reached the end of the line. Well it's allllllllright... ridin' around in the breeze...
        if loc == end:
            # If the cost is lower than the current min cost then that's the best path
            if min_cost is None or cost <= min_cost:
                min_cost = cost
                # Store the best paths for part 2
                if cost not in best_paths:
                    best_paths[cost] = set()
                best_paths[cost].update(set(newpath))
                #print(min_cost)
            continue
        # Been here before?
        if (loc,dir) in SEEN: continue
        # Nope, new location
        _SEEN = copy.copy(SEEN)
        _SEEN.add((loc,dir))
        # Add the cost for this node
        nodes[(loc,dir)] = cost
        # Current r,c
        r,c = loc
        # Try to go forward, left and right
        for dr,dc in [dir, LEFT[dir], RIGHT[dir]]:
            cost_add = 1
            newloc = (r+dr,c+dc)
            newdir = (dr,dc)
            if newloc not in walls:
                # Cost is an extra +1000 if we didn't go in the same direction as last time
                if dir != newdir:
                    cost_add += 1000
                heapq.heappush(Q, (newloc, cost+cost_add, _SEEN, newdir, newpath) )

    return min_cost, best_paths

min_cost, paths = solve(S,E)

print('Part 1:', min_cost)
print('Part 2:', len(paths[min_cost]))
