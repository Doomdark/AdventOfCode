from collections import defaultdict
import heapq as heap

walls = set()
num = 1364

max_x = 35
max_y = 45

def adjacents(x,y):
    l = []
    if x-1 >=    0: l.append((x-1,y))
    if x+1 < max_x: l.append((x+1,y))
    if y-1 >=    0: l.append((x,y-1))
    if y+1 < max_y: l.append((x,y+1))
    return l

def is_wall(x,y,num):
    a = x*x + 3*x + 2*x*y + y + y*y + num
    bits = 0
    while a > 0:
        if a&1:
            bits += 1
        a >>= 1
    if bits % 2 == 1:
        return True
    return False

# Make the grid of walls
for x in range(max_x):
    for y in range(max_y):
        if is_wall(x,y,num):
            walls.add((x,y))

def draw_grid():
    for y in range(max_y):
        line = ''
        for x in range(max_x):
            if (x,y) in walls:
                line += '#'
            else:
                line += '.'
        print(line)

#draw_grid()

# Construct a weighted graph of the adjacent nodes for a space
G = {}
for x in range(max_x):
    for y in range(max_y):
        for _x,_y in adjacents(x,y):
            # If the adjacent node isn't a wall then we can visit it
            if (_x,_y) not in walls:
                if (x,y) not in G:
                    G[(x,y)] = {}
                G[(x,y)][(_x,_y)] = 1

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

parentsMap, nodeCosts = dijkstra(G, (1,1))
print("Part 1:", nodeCosts[(31,39)])

# How many locations can you reach in upto 50 steps?
locs = 0
for node, steps in nodeCosts.items():
    if steps <= 50:
        locs += 1
print("Part 2:", locs)
