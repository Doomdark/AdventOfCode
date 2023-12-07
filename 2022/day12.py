from collections import defaultdict
import heapq as heap

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


grid = {}
max_x = 0
max_y = 0

def adjacents(x,y):
    sheight = grid[(x,y)]

    # Return the possible adjacent squares
    possibles = []
    if x-1 >= 0:    possibles.append((x-1,y))
    if x+1 < max_x: possibles.append((x+1,y))
    if y-1 >=    0: possibles.append((x,y-1))
    if y+1 < max_y: possibles.append((x,y+1))

    l = []
    # Now discard the adjacents that are too much higher than the current square
    for p in possibles:
        nx,ny = p
        fheight = grid[(nx,ny)]
        if fheight <= (sheight + 1):
            l.append((nx,ny))
    return l

lines = open("12.in").read().splitlines()

# Store info about the map
x = 0
y = 0
S = None
E = None

# Part 2
all_a = []

# Construct the map
for line in lines:
    x = 0
    for char in line:
        if char == 'S':
            S = (x,y)
            grid[(x,y)] = ord('a')
        elif char == 'E':
            E = (x,y)
            grid[(x,y)] = ord('z')
        else:
            grid[(x,y)] = ord(char)
            # Part 2
            if char == 'a':
                all_a.append((x,y))
        x += 1
    y += 1

# Store the maximum extents
max_x = x
max_y = y

# Construct the connectivity graph
G = {}
for x in range(max_x):
    for y in range(max_y):
        # Make a node
        if (x,y) not in G:
            G[(x,y)] = {}
        # Add the adjacents to the node
        for _x,_y in adjacents(x,y):
            G[(x,y)][(_x,_y)] = 1

parentsMap, nodeCosts = dijkstra(G, S)
print("Part 1:", nodeCosts[E])

## Part 2 ##
shortest_a = 9999999

# Find the shortest path from any 'a' square
for a in all_a:
    parentsMap, nodeCosts = dijkstra(G, a)
    dist = nodeCosts[E]
    if dist < shortest_a:
        shortest_a = dist

print('Part 2:', shortest_a)
