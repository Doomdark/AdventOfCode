from collections import  defaultdict, deque
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

def md(a,b):
    'Manhattan distance'
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Store where everything is
walls   = set()
elves   = defaultdict(int)
goblins = defaultdict(int)

# Different attack powers in part 2
goblin_attack_power = 3
elf_attack_power = 3

# Maybe be verbose about stuff
move_verbose = False
attack_verbose = False
grid_verbose = True

# Read the input
lines = open("15.in").read().splitlines()

for r,row in enumerate(lines):
    for c,col in enumerate(row):
        loc = (r,c)
        if   col == '#': walls.add(loc)
        elif col == 'G': goblins[loc] = 200
        elif col == 'E': elves[loc] = 200

# Max grid sizes
R = r+1
C = c+1

# Copy the start positions for part 2
elves_copy   = copy.deepcopy(elves)
goblins_copy = copy.deepcopy(goblins)

filenames = []

# Draw the current state
def draw_grid(iteration=0,to_file=False):
    global walls,elves,goblins,R,C,filenames
    S = ''
    S += '----- Iteration {} -----\n\n'.format(iteration)
    for r in range(R):
        row = ''
        row_vals = []
        for c in range(C):
            if   (r,c) in walls:row += '#'
            elif (r,c) in goblins:
                row += 'G'
                row_vals.append('G({})'.format(goblins[(r,c)]))
            elif (r,c) in elves:
                row += 'E'
                row_vals.append('E({})'.format(elves[(r,c)]))
            else:                  row += '.'

        S += '{}'.format(row) + ' ' + ', '.join(row_vals) + '\n'

    if to_file:
        filename = '15_iter_{:02}.txt'.format(iteration)
        with open(filename,'w') as f:
            f.write(S)
        filenames.append(filename)
    else:
        print(S)

# Get the adjacent locations which aren't walls
def get_adjacents(loc):
    global R,C
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

# Get all the paths from start to the multiple endpoints which are of the specified length, avoiding some locations.
def get_all_shortest_paths(start,ends,length,avoid=set()):
    # Store the shortest paths
    paths = []
    # Keep a dictionary of the visited locations
    visited = defaultdict(lambda: 100000000)
    visited[start] = 0
    # Store the currently active paths
    q = deque()
    q.append((start,0,[]))

    if move_verbose: print('GSP:',start,ends,length)

    while q:
        cur_loc, cur_len, cur_path = q.pop()

        # Reached an end
        if cur_loc in ends:
            paths.append(cur_path)
        # Gone as far as we should have without reaching an end point
        elif cur_len == length:
            pass
        # Maybe go somewhere else
        else:
            # Where can we go from here?
            for adj in G[cur_loc].keys():
                # Can only go to unoccupied squares, or it's the endpoint.
                if adj in ends or adj not in avoid:
                    new_loc = adj
                    new_len = cur_len+1
                    new_path = cur_path + [new_loc]
                    new_dist = length-new_len
                    # Is the new length going to be <= any existing visit? Go there if so.
                    # Also use the Manhattan distance to the endpoints to ensure the path doesn't stray wildly.
                    # The Manhattan distance is the longest possible distance from this point.
                    if visited[adj] >= new_len and any([md(adj,end) <= new_dist for end in ends]):
                        # Add the new location
                        q.append((new_loc, new_len, new_path))
                        visited[adj] = new_len

    return paths

# Get the "reading order" next location from the current location and provided next location choices
def get_reading_order(loc, steps):
    r,c = loc
    # Start as the next step being on the far side of the grid.
    Nr,Nc = R,C
    # Look at the first step on each of the paths
    for step in steps:
        nr,nc = step
        # Check if the row is more negative than the current row. If it is then choose that.
        if nr < Nr: Nr,Nc = nr,nc
        elif nr == Nr and nc < Nc: Nr,Nc = nr,nc
    return (Nr,Nc)

# Solve the puzzle
def solve(elves,goblins,to_file=False):
    global R,C,G

    iterations = 0

    while len(elves) > 0 and len(goblins) > 0:
        moved = set()

        # Iterate over the grid
        for r in range(R):
            for c in range(C):
                loc = (r,c)
                # Skip this one if it has already moved
                if loc in moved: continue

                # Is this location an elf or goblin?
                if loc in set(elves.keys()) | set(goblins.keys()):
                    enemies = elves
                    if loc in elves:
                        enemies = goblins

                    # Any enemies left?
                    if not enemies: return iterations

                    nearest = 100000000
                    nearest_loc = None
                    nloc = loc

                    # Is there an enemy on an adjacent location?
                    adjacents = G[loc].keys()
                    if move_verbose: print('-'*5,loc)
                    if move_verbose: print('Enemies  :',enemies)
                    if move_verbose: print('Adjacents:',adjacents)

                    # No enemy nearby so move instead
                    if not any([True for x in adjacents if x in enemies]):

                        # Get all the distances from the start point to all adjacent places,
                        # making sure we avoid the current elves and goblins.
                        parentsMap, nodeCosts, paths = dijkstra(G,loc,set(elves.keys())|set(goblins.keys()))

                        # Get all the enemies' adjacent locations
                        adjacents = []
                        for enemy in enemies:
                            adjacents.extend(get_adjacents(enemy))

                        # Only allow adjacent squares that are reachable, so they must be in the dijkstra output
                        valid_adjacents = [x for x in adjacents if x in nodeCosts]

                        # If there are no valid adjacent squares then go onto the next elf/goblin
                        if not valid_adjacents: continue

                        # What are the nearest adjacent squares?
                        nearest = 100000000
                        nearest_locs = set()
                        for adj in valid_adjacents:
                            # Nearest match
                            if nodeCosts[adj] == nearest:
                                nearest_locs.add(adj)
                            # New nearest
                            elif nodeCosts[adj] < nearest:
                                nearest = nodeCosts[adj]
                                nearest_locs = {adj}

                        if move_verbose: print('Nearest enemy adjacent to {} is {}:{}'.format(loc,nearest_locs,nearest))

                        # Find all the paths which are of the same length as the nearest location
                        all_paths = get_all_shortest_paths(loc,nearest_locs,nearest,set(elves.keys())|set(goblins.keys()))
                        # Get the next location to move to from the reading order
                        nloc = get_reading_order(loc, [x[0] for x in all_paths])

                        # Move the current guy
                        if loc in elves:
                            if move_verbose: print("Moving Elf from {} to {}".format(loc,nloc))
                            hp = elves[loc]
                            del elves[loc]
                            elves[nloc] = hp
                        else:
                            if move_verbose: print("Moving Goblin from {} to {}".format(loc,nloc))
                            hp = goblins[loc]
                            del goblins[loc]
                            goblins[nloc] = hp

                        # Don't move this one again this turn
                        moved.add(nloc)

                    # Now we've moved (or not) check for enemies and attack them if there is one nearby
                    adjacents = set(G[nloc].keys())
                    enemies = set()
                    baddies = None
                    # Get adjacent enemies
                    if nloc in elves:
                        enemies = adjacents & set(goblins.keys())
                        baddies = goblins
                    else:
                        enemies = adjacents & set(elves.keys())
                        baddies = elves

                    if attack_verbose: print(nloc, "AE:",enemies)

                    if enemies:
                        # Choose the enemy with the fewest HP to hit
                        targets = []
                        lowest_hp = 1000000
                        for enemy in enemies:
                            hp = baddies[enemy]
                            if hp == lowest_hp:
                                targets.append(enemy)
                            elif hp < lowest_hp:
                                targets = [enemy]
                                lowest_hp = hp
                        target = get_reading_order(nloc, targets)
                        # Attack!
                        if attack_verbose: print('ATTACK: {} -> {}'.format(nloc, target))
                        attack_power = elf_attack_power
                        if baddies == elves:
                            attack_power = goblin_attack_power
                        baddies[target] -= attack_power
                        if baddies[target] <= 0:
                            del baddies[target]
        iterations += 1
        if grid_verbose: draw_grid(iterations, to_file)

    return iterations

## Part 1 ##

to_file = False
do_part1 = True

if do_part1:
    # Solve
    if grid_verbose: draw_grid(0,to_file)
    iterations = solve(elves,goblins,to_file)
    # Part 1 has the goblins winning
    remaining_hp = sum(goblins.values())
    print('Part 1:', iterations*remaining_hp)

if to_file:
    try:
        import os
        filenames = [('15_iter_{:02}.txt'.format(x)) for x in range(0,83)]
        os.environ['T2G_DEFAULT_FONT_SIZE'] = "14"
        os.system('t2g --input {} --output 15_part1.gif --duration 0.50 --frame {}'.format(os.getcwd(), len(filenames)))
    except:
        pass

## Part 2 ##

do_part2 = True

if do_part2:

    # Start at a highish attack power
    elf_attack_power = 15

    while True:
        print('-'*5,'Elf attack power:',elf_attack_power,'-'*5)
        # Restore the start state
        elves = copy.deepcopy(elves_copy)
        goblins = copy.deepcopy(goblins_copy)
        # Run the solver
        iterations = solve(elves,goblins)
        # Maybe draw the grid
        if grid_verbose: draw_grid(iterations)
        # If there are no goblins left and we didn't lose any elves then that's the end
        if not goblins and len(elves) == len(elves_copy):
            break
        # Increment the attack power for next time
        elf_attack_power += 1

    remaining_hp = sum(elves.values())
    print('Part 2:', iterations*remaining_hp)
