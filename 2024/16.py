from collections import defaultdict
import heapq

lines = open('16.in').read().splitlines()

S = None
E = None

for r,line in enumerate(lines):
    for c,char in enumerate(line):
        if   char == 'S': S = (r,c)
        elif char == 'E': E = (r,c)

LEFT  = {(-1,0):(0,-1), (0,-1):(1,0), (1,0):(0,1), (0,1):(-1,0)}
RIGHT = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}

def solve(start, end):
    Q = []
    heapq.heappush(Q, (0, start, (0,1), []) )

    min_cost = 9999999999
    min_paths = None
    nodes = defaultdict()

    while Q:
        cost, loc, dir, path = heapq.heappop(Q)
        # If the path cost is already higher than the min cost then this path is bogus
        if cost > min_cost:
            continue
        # Have we reached here before?
        if (loc,dir) in nodes:
            # If the current cost on entering from the same direction is higher than however we got here before then ignore this path
            if cost > nodes[(loc,dir)]: continue
        # Accumulate the path
        newpath = path + [loc]
        # Reached the end of the line. Well it's allllllllright... ridin' around in the breeze...
        if loc == end:
            # If the cost is lower than the current min cost then that's the best path
            if cost < min_cost:
                min_cost = cost
                # Store the best paths for part 2
                min_paths = set(newpath)
            else: # Same cost
                min_paths.update(set(newpath))
            continue
        # Add the cost for this node
        nodes[(loc,dir)] = cost
        # Current r,c
        r,c = loc
        # Try to go forward, left and right
        for dr,dc in [dir, LEFT[dir], RIGHT[dir]]:
            cost_add = 1
            nr,nc = r+dr,c+dc
            newdir = (dr,dc)
            if lines[nr][nc] != '#':
                # Cost is an extra +1000 if we didn't go in the same direction as last time
                if dir != newdir:
                    cost_add += 1000
                heapq.heappush(Q, (cost+cost_add, (nr,nc), newdir, newpath) )

    return min_cost, min_paths

min_cost, paths = solve(S,E)

print('Part 1:', min_cost)
print('Part 2:', len(paths))
