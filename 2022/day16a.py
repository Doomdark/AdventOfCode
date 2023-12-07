from collections import defaultdict, deque
import heapq as heap
import copy
import hashlib

lines = open("16.ex").read().splitlines()

def dijkstra(G, startingNode):
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
            if adjNode in visited:  continue

            newCost = nodeCosts[node] + weight
            if nodeCosts[adjNode] > newCost:
                parentsMap[adjNode] = node
                nodeCosts[adjNode] = newCost
                paths[adjNode] = path
                heap.heappush(pq, (newCost, adjNode, path + [adjNode]))

    return parentsMap, nodeCosts, paths

class Valve:
    def __init__(self, name, rate, dests):
        self.name = name
        self.rate = rate
        self.dests = dests
        self.open = False
        self.count = 0

    def openable(self):
        return not self.open and self.rate>0

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

valves_copy = copy.deepcopy(valves)

# Construct the connectivity graph
G = {}
for x in valves:
    # Make a node
    if x not in G:
        G[x] = {}
    # Add the adjacents to the node
    for dest in valves[x].dests:
        G[x][dest] = 1

# For all valves make a list of how far it is to all other valves
R = defaultdict(dict)
P = defaultdict(dict)
for v in valves:
    parentMap, nodeCosts, paths = dijkstra(G, v)
    for vv in valves:
        if v == vv:
            continue
        R[v][vv] = nodeCosts[vv]
        P[v][vv] = paths[vv] + [vv]

#for k,v in P.items():
#    print(k,v)
#for k,v in R.items():
#    print(k,v)

def solve(time_limit=30):
    # Valves to open
    valves_to_open = {k:v for k,v in valves.items() if v.openable()}
    open_valves    = {}

    # Start state. Path, Time, Open Valves
    s = [[['AA'], 0, open_valves]]

    max_pressure = 0
    # Keep going until we run out of states
    while s:
        # Get the state
        path, time, open_valves = s.pop()
        # This is the valve where we are at the moment
        current_valve = path[-1]

        # Have we run out of time? Or run out of valves to open?
        if time >= time_limit or len(path) == len(valves_to_open) + 1:
            pressure = 0

            # For each valve in the open valves list add on the total pressure released
            for valve, opening_time in open_valves.items():
                # Make sure this is never below 0
                open_for = max(time_limit - opening_time, 0)
                pressure += open_for*valves[valve].rate

            # Keep track of the maximum pressure on any of the paths
            max_pressure = max(pressure, max_pressure)
        else:
            # Travel to the open valves
            for next_valve in valves_to_open:
                # Is the next valve open?
                if next_valve not in open_valves:
                    # How long does it take to get there?
                    travel_time = R[current_valve][next_valve]
                    # New time
                    new_time = time + travel_time + 1 # 1 for opening the valve
                    # Add the valve to the open valves list. Make a copy to avoid corruption.
                    new_open_valves = copy.deepcopy(open_valves)
                    new_open_valves[next_valve] = new_time
                    # Add this valve to the path list. Copy the path list first.
                    new_path = list(path)
                    new_path.append(next_valve)
                    # Add this as a new state
                    s.append([new_path, new_time, new_open_valves])

    return max_pressure

print('Part 1:', solve(30))

## Part 2 ##

# Solve for 26 minutes and get all the path combinations that don't overlap

open_valves = {}
open_valves_bitmask = 0
open_valves_times   = tuple([0] * len(valves_to_open))
valve_nums = {}
valve_nums_rev = {}
for num,k in enumerate(valves_to_open.keys()):
    valve_nums[k] = num
    valve_nums_rev[num] = k

# [Current state, valve path, Target valve]. Time, Open Valves bitmask,, open valves times
s = deque()
s.append(([tuple(['AA']), 0], [tuple(['AA']), 0], 0, open_valves_bitmask, open_valves_times))

# We've got this long
time_limit = 26

#print(len(valves_to_open.keys()))

# This is the released pressure
max_pressure = 0

seen = set()

def update2(who, time, bloke, open_valves_bitmask, open_valves_times):
    global valves_to_open, R

    path        = bloke[0]
    target_time = bloke[1]

    # Store new states
    ns = deque()

    # Have we reached the valve target time?
    if time == target_time:
        # The destination valve
        current_valve = path[-1]
        # Travel to the open valves
        for next_valve in valves_to_open:
            # Is the next valve open?
            next_valve_num = valve_nums[next_valve]
            next_valve_open = (open_valves_bitmask >> next_valve_num) & 0x1
            if not next_valve_open and next_valve != current_valve:
                # How long does it take to get there?
                #print(who,target_time,time, current_valve, next_valve)
                travel_time = R[current_valve][next_valve]
                # New time
                new_time = time + travel_time + 1 # 1 for opening the valve
                # Add the valve to the open valves list. Make a copy to avoid corruption.
                new_open_valves_bitmask = copy.deepcopy(open_valves_bitmask)
                new_open_valves_times   = list(copy.deepcopy(open_valves_times))
                new_open_valves_bitmask |= 1<<next_valve_num
                #print(bin(new_open_valves_bitmask))
                new_open_valves_times[next_valve_num] = new_time
                # Add this valve to the path list. Copy the path list first.
                new_path = list(path)
                new_path.append(next_valve)
                # Add this as a new state
                ns.append([new_path, new_time, new_open_valves_bitmask, new_open_valves_times])
    else: # Not there yet
        ns.append([path, target_time, open_valves_bitmask, open_valves_times])

    return ns

seen = set()

# Keep going until we run out of states
while len(s):

    #print(len(s))

    # Get the state. Use pop() rather than popleft() so we do the oldest states first and don't amass a zillion states
    me, el, time, open_valves_bitmask, open_valves_times = s.pop()
    #print(len(s), time, bin(open_valves_bitmask), max_pressure)

    # Have we run out of time? Or run out of valves to open?
    if time >= time_limit or (str(bin(open_valves_bitmask))[2:].count('1') == len(valves_to_open)):
        pressure = 0
        open_valves_flows = [0] * len(valves_to_open)

        # For each valve in the open valves list add on the total pressure released
        for num,t in enumerate(open_valves_times):
            # Check the valve has been opened
            if (open_valves_bitmask >> num) & 0x1:
                #print(num, valve_nums_rev[num], time)
                # Make sure this is never below 0
                open_for = max(time_limit - t, 0)
                flow = open_for*valves[valve_nums_rev[num]].rate
                open_valves_flows[num] = flow
                pressure += flow

        # Keep track of the maximum pressure on any of the paths
        last_max_pressure = int(max_pressure)
        max_pressure = max(pressure, max_pressure)
        if last_max_pressure != max_pressure:
            print(time, time_limit, bin(open_valves_bitmask), max_pressure, str(bin(open_valves_bitmask))[2:].count('1'), len(valves_to_open), open_valves_times, open_valves_flows)
        #exit(0)
        #exit(0)
    else:
        # In case we want to modify the open valves
        new_open_valves_bitmask = copy.deepcopy(open_valves_bitmask)
        new_open_valves_times   = list(copy.deepcopy(open_valves_times))

        # Calculate new states for me and elephant, and update the open valves
        if me[1] == time:
            me_ns = update2('me', time, me, open_valves_bitmask, new_open_valves_times)
            el_ns = update2('el', time, el, open_valves_bitmask, new_open_valves_times)
        else:
            el_ns = update2('el', time, el, new_open_valves_bitmask, new_open_valves_times)
            me_ns = update2('me', time, me, new_open_valves_bitmask, new_open_valves_times)

        # Get the permutations of the me_ns and el_ns to determine all possible new states
        #if not me_ns: me_ns.append([me[0],me[1],open_valves_bitmask,open_valves_times])
        #el_ns = []
        #el_ns.append([el[0],el[1],open_valves_bitmask,open_valves_times])

        for m in me_ns:
            _me_path, _me_target_time, _me_open_valves_bitmask, _me_open_valves_times = m
            for e in el_ns:
                _el_path, _el_target_time, _el_open_valves_bitmask, _el_open_valves_times = e
                # Combine the open valves states
                new_open_valves_bitmask = _me_open_valves_bitmask | _el_open_valves_bitmask
                new_open_valves_times = []
                for a,b in zip(_me_open_valves_times, _el_open_valves_times):
                    if a == 0 or b == 0:
                        new_open_valves_times.append(max(a,b))
                    else:
                        new_open_valves_times.append(min(a,b))
                    #new_open_valves_times   = tuple([max(a,b) for a,b in zip(_me_open_valves_times, _el_open_valves_times)])
                #print(time, m, e, new_open_valves)
                #print('. ',valves_to_open)
                assert time <= _me_target_time
                assert time <= _el_target_time
                # Stop at the first scheduled state first
                new_time = min(_me_target_time, _el_target_time)
                state = ((tuple(_me_path), _me_target_time),
                         (tuple(_el_path), _el_target_time),
                         new_time,
                         new_open_valves_bitmask,
                         tuple(new_open_valves_times))
                seen_key = (new_time,
                            new_open_valves_bitmask,
                            tuple(new_open_valves_times))
                if state in seen:
                    continue
                seen.add(state)
                s.append(state)

print('Part 2:',max_pressure)
