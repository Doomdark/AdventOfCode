import copy
from collections import deque

lines = open("16.ex").read().splitlines()

class Valve:
    def __init__(self, name, rate, tunnels):
        self.name = name
        self.rate = rate
        self.tunnels = tunnels
        self.open = False
        self.count = 0

    def update(self):
        if self.open:
            self.count += self.rate

    def openable(self):
        return not self.open and self.rate>0

    def __str__(self):
        return '* {}: {}'.format(self.name, self.count)

valves = {}

for line in lines:
    l = line.split('; ')
    ll = l[0].split(' ')
    valve = ll[1]
    rate = int(ll[4].split('=')[1])
    ll = l[1].split()
    tunnels = [x.replace(',','') for x in ll[4:]]
    v = Valve(valve,rate,tunnels)
    valves[valve] = v

# This is where the BFS has got to
new_states = deque()
# These states don't have all their valves open
states = []
# These states do have all their valves open
all_open_states = []

current_states = deque()
# Keep track of all visited states
current_states.append(('AA', valves))

# We've got 30 minutes
for minute in range(30):

    print('Minute',minute+1, len(current_states))

    # Update valves in all states
    for loc,valves in all_open_states + states + list(current_states):
        # Update the valve flow counts
        for n,valve in valves.items():
            valve.update()

    # Really new states
    new_states = deque()

    # Only look at new_states to get the next moves
    while current_states:
        # Get the first new state from last time
        loc,valves = current_states.popleft()

        # Are all the valves open now?
        if all([v.open for k,v in valves.items()]):
            continue

        # Copy the valves to avoid tragedy
        _valves = copy.deepcopy(valves)

        # Get the current valve from the dictionary
        valve = _valves[loc]
        #print(valve)

        # We could carry on and not open this valve
        for adj in valve.tunnels:
            # If the valve destination is not openable then don't go there
            if (adj, _valves) not in new_states:
                new_states.append((adj, _valves))

        # If this valve has yet to be opened then we can do that and wait here
        if valve.openable():
            #print(valve.name, "Opening ",valve.name)
            valve.open = True
            __valves = copy.deepcopy(_valves)
            new_states.append((valve.name, __valves))

    # Check all the old states to see if they have all their valves open already
    new_old_states = []
    for loc,valves in states + list(new_states):
        state = (loc,valves)
        done_state = False
        for n,valve in valves.items():
            # This valve still isn't open
            if valve.openable():
                new_old_states.append(state)
                done_state = True
                break
        # All the valves are open for this state
        if not done_state:
            all_open_states.append(state)

    # Only check the queues for states where not all the valves are open
    states = new_old_states

    # Newer states for next loop
    current_states = new_states

print('States:',len(states))

# Find the state with the largest cumulative flow
flows = []
for q,valves in states:
    flows.append(sum([v.count for n,v in valves.items()]))

print(max(flows))
