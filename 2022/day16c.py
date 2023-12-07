from collections import defaultdict, deque
import heapq as heap

lines = open("16.in").read().splitlines()

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

class Valve:
    def __init__(self, name, rate, dests):
        self.name = name
        self.rate = rate
        self.dests = dests
        self.count = 0

    def openable(self):
        return self.rate>0

    def __repr__(self):
        return '* {}: {}: {}: {}'.format(self.name, self.rate, self.count, self.open)

valves = {}

for line in lines:
    l = line.split('; ')
    ll = l[0].split(' ')
    valve = ll[1]
    rate = int(ll[4].split('=')[1])
    ll = l[1].split()
    dests = [x.replace(',','') for x in ll[4:]]
    v = Valve(valve,rate,dests)
    valves[valve] = v

# Construct the connectivity graph
G = defaultdict(dict)
for x in valves:
    # Make a node and sdd the adjacents to the node
    for dest in valves[x].dests:
        G[x][dest] = 1

# For all valves make a list of how far it is to all other valves
R = defaultdict(dict)
for v in valves:
    parentMap, nodeCosts = dijkstra(G, v)
    for vv in valves:
        if v == vv:
            continue
        R[v][vv] = nodeCosts[vv]


def solve(time=30):
    # Valves to open
    valves_to_open = {k:v for k,v in valves.items() if v.openable()}
    visited        = defaultdict(int)
    solutions      = defaultdict(int)

    # Start state. Path, Time, Open Valves, Pressure
    s = deque()
    # Add the initial state. Must use a frozenset for it to be used in the solutions dict.
    s.append(('AA', time, frozenset(), 0))

    # Keep going until we run out of states
    while s:
        # Get the state
        current_valve, time, open_valves, pressure = s.pop()

        # Store the max pressure for the open valves to this point
        solutions[open_valves] = max(solutions[open_valves], pressure)

        # Search for the next valves to travel to
        for next_valve in valves_to_open:
            if next_valve not in open_valves:
                # How long does it take to get there?
                travel_time = R[current_valve][next_valve]
                # New time
                new_time = time - travel_time - 1 # 1 for opening the valve
                # Add the valve to the open valves set
                new_open_valves = open_valves | {next_valve}
                # Add on the pressure added by opening this valve at this time
                new_pressure = pressure + new_time * valves[next_valve].rate
                # Can we visit more valves after this?
                visited_key = (next_valve, new_open_valves)
                # Check if the next state has already been visited and if it had a higher pressure previously
                if new_time > 0 and visited[visited_key] < new_pressure:
                    visited[visited_key] = new_pressure
                    s.append((next_valve, new_time, new_open_valves, new_pressure))

    return solutions

solutions = solve(30)

print('Part 1:',max(solutions.values()))

## Part 2 ##

# Solve for 26 minutes and get all the path combinations

from itertools import combinations

# Solve it once and find all the unique combinations of paths
solutions = solve(26)

# Check no duplicate valves are in the two path sets as the 2 sets of valves must be unique
max_pressure = max(p1 + p2 for (s1,p1),(s2,p2) in combinations(solutions.items(), 2) if not s1.intersection(s2))
print('Part 2:', max_pressure)
