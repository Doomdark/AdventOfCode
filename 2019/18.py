from collections import defaultdict, deque
import heapq as heap
import copy

def dijkstra(G, startingNode, avoid=set()):
    visited = set()
    parentsMap = {}
    pq = []
    nodeCosts = defaultdict(lambda: float('inf'))
    nodeCosts[startingNode] = 0
    paths = {}
    heap.heappush(pq, (0, startingNode, []))

    while pq:
        # go greedily by always extending the shorter cost nodes first
        _, node, path = heap.heappop(pq)
        visited.add(node)

        for adjNode, weight in G[node].items():
            if adjNode in visited: continue
            if adjNode in avoid: continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                parentsMap[adjNode] = node
                nodeCosts[adjNode] = newCost
                adjPath = path + [adjNode]
                paths[adjNode] = path
                heap.heappush(pq, (newCost, adjNode, adjPath))

    return parentsMap, nodeCosts, paths

walls = set()
doors = defaultdict(int)
keys  = defaultdict(int)

start = (0,0)

lines = open('18.in').read().splitlines()

R = 0
C = 0

for r,row in enumerate(lines):
    for c,col in enumerate(row):
        loc = (r,c)
        if   col == '#' : walls.add(loc)
        elif col == '@' : start = loc
        elif ord(col) in range(ord('a'),ord('z')+1): keys[loc] = col
        elif ord(col) in range(ord('A'),ord('Z')+1): doors[loc] = col

R = r+1
C = c+1

# Draw the current state
def draw_grid():
    global walls,doors,keys
    for r in range(R):
        row = ''
        for c in range(C):
            loc = (r,c)
            if   loc in walls: row += '#'
            elif loc == start: row += '@'
            elif loc in keys:  row += keys[loc]
            elif loc in doors: row += doors[loc]
            else:              row += '.'
        print(row)

draw_grid()

# Get the adjacent locations which aren't walls
def get_adjacents(loc):
    adjacents = []
    r,c = loc
    for dr,dc in [(-1,0),(1,0),(0,1),(0,-1)]:
        nr,nc = r+dr,c+dc
        if (nr,nc) not in walls:
            adjacents.append((nr,nc))
    return adjacents

# Make a connectivity graph
G = defaultdict(dict)
for r in range(R):
    for c in range(C):
        if (r,c) in walls: continue
        adjacents = get_adjacents((r,c))
        for adj in adjacents:
            G[(r,c)][adj] = 1

# For all keys make a list of how far it is to all other keys, ignoring blockages
Mins = defaultdict(lambda:100000000)
min_steps_between_keys = 1000000
for k in keys:
    parentMap, nodeCosts, paths = dijkstra(G, k)
    for kk in keys:
        if k == kk:
            continue
        min_steps_between_keys = min(min_steps_between_keys, nodeCosts[kk])
        Mins[k] = min(Mins[k],nodeCosts[kk])

def solve():
    global R,C,G

    q = deque()
    # Current loc, steps, owned keys, open doors
    q.append( ( start, 0, frozenset(), frozenset() ) )
    visited = defaultdict(lambda:10000000)

    min_steps = 10000000

    while q:
        cur_loc, cur_steps, cur_keys, open_doors = q.pop()
        print(len(q), min_steps, cur_steps, len(cur_keys), len(open_doors))

        # Any more keys to collect?
        if len(cur_keys) == len(keys):
            if cur_steps < min_steps:
                print(cur_steps),
            min_steps = min(min_steps, cur_steps)

        else: # More keys to collect
            # How many keys left?
            keys_left = [kloc for kloc,v in keys.items() if v not in cur_keys]
            min_steps_remaining = sum([Mins[k] for k in keys_left])
            # If the number of keys left * min distance between keys + cur_steps > min steps then stop here
            if (cur_steps + min_steps_remaining) >= min_steps:
                continue
            # Get paths from here to everywhere avoiding the closed doors
            parentsMap, nodeCosts, paths = dijkstra(G,cur_loc,set(doors.keys())-open_doors)
            # Iterate through the keys
            for key_loc,key in keys.items():
                # If we've got this key then skip it
                if key in cur_keys:
                    continue
                # Can get to this key?
                if key_loc in nodeCosts:
                    #print('Cost to', key, nodeCosts[key_loc])
                    new_steps  = cur_steps + nodeCosts[key_loc]
                    # Already gone further than the current min_steps
                    if new_steps >= min_steps:
                        continue
                    new_loc = key_loc
                    new_open_doors = copy.copy(open_doors)
                    # Add the corresponding door to the open doors list
                    for door_loc,door in doors.items():
                        if ord(key)-32 == ord(door):
                            new_open_doors = open_doors | {door_loc}
                            break
                    new_keys = cur_keys | {key}
                    new_state = (new_loc, new_keys)
                    if visited[new_state] > new_steps:
                        q.append((new_loc, new_steps, new_keys, new_open_doors))
                        visited[new_state] = new_steps

    return min_steps

def got_key(keys, door):
    for key in keys:
        if ord(key)-32 == ord(door):
            return True
    return False

def solve2():
    q = deque()
    visited = defaultdict(lambda:10000000)
    q.append((start, 0, frozenset()))
    min_steps = 100000000

    while q:
        cur_loc, cur_steps, cur_keys = q.popleft()
        #print(len(q), cur_loc, cur_steps, cur_keys, len(cur_keys))

        # Found a key!
        if cur_loc in keys:
            cur_keys = cur_keys | {keys[cur_loc]}
            # Any more keys to collect?
            if len(cur_keys) == len(keys):
               return cur_steps
        # Got to a door but can't open it
        elif cur_loc in doors and not got_key(cur_keys, doors[cur_loc]):
            continue

        # More keys needed
        state = (cur_keys, cur_loc)
        # Got to this state before in fewer steps
        if visited[state] < cur_steps:
            continue
        # Update the step count
        visited[state] = cur_steps

        for loc in get_adjacents(cur_loc):
            q.append((loc, cur_steps+1, cur_keys))

min_steps = solve()
print('Part 1:', min_steps)
