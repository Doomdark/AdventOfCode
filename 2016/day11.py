from collections import deque
from itertools import combinations
import copy
from sortedcontainers import SortedList
import pickle

floors = {}

floors[1] = SortedList(['tg', 'tm', 'pg', 'sg'])
floors[2] = SortedList(['pm', 'sm'])
floors[3] = SortedList(['prg', 'prm', 'rg', 'rm'])
floors[4] = SortedList([])

# Example
floors[1] = ['hm', 'lm']
floors[2] = ['hg']
floors[3] = ['lg']
floors[4] = []

# How many generators are there? Everything is in pairs.

total = sum([len(v) for v in floors.values()])

def solve(part2=False):
    global floors
    if part2:
        floors[1].update(['em','eg','dm','dg'])
    q = deque()
    q.append((0, 1, floors)) # Start on floor 1
    # Store all previous states to eliminate repeats
    states = set()
    start_state = (1, str(floors))
    #print(start_state)
    #exit(1)
    states.add(start_state)

    while q:
        moves, floor, _floors = q.popleft()
        #print(len(q), len(states), moves, floor, _floors)
 
        # Check for the end
        if len(_floors[4]) == total:
            return(moves)

        # What moves can we do with the elevator?
        eposs = []
        for de in [1,-1]:
            ne = floor + de
            if 1<=ne<=4:
                empty = False
                # if the lower floors are empty then don't move down
                if de == -1 and ne > 1:
                    empty = True
                    for f in range(1,ne):
                        if len(_floors[f]) > 0:
                            empty = False
                if (de == 1) or (empty == False):
                    eposs.append(ne)

        # For each destination, what can we move that doesn't violate the rules?
        # 1. Move either 1 or 2 things.
        # 2. M can't be on floor with a different G.
        movable = set(_floors[floor])
        # Get all possible combinations of movable things. Either 1 or 2 things can move at a time.
        combs = [com for sub in range(2) for com in combinations(movable, sub + 1)]
        # Iterate through each destination floor and try to move each combination of things
        for ne in eposs:
            for comb in combs:
                __floors = copy.deepcopy(_floors)
                fail = False
                
                # Make the set of items for the new floor
                new_floor = SortedList(set(__floors[ne])    | set(comb))
                old_floor = SortedList(set(__floors[floor]) - set(comb))
                
                # Make a list of generators and microchips on the new and old floors
                new_generators = [x for x in new_floor if x[-1] == 'g']
                new_microchips = [x for x in new_floor if x[-1] == 'm']
                old_generators = [x for x in old_floor if x[-1] == 'g']
                old_microchips = [x for x in old_floor if x[-1] == 'm']
                
                # For each new floor microchip check if its generator is here
                for chip in new_microchips:
                    prefix = chip[:-1]
                    # If the generator for this microchip is not on this floor but another generator is then fail
                    if '{}g'.format(prefix) not in new_floor and len(new_generators) > 0:
                        fail = True

                # For each old floor microchip check if its generator is here
                for chip in old_microchips:
                    prefix = chip[:-1]
                    # If the generator for this microchip is not on this floor but another generator is then fail
                    if '{}g'.format(prefix) not in old_floor and len(old_generators) > 0:
                        fail = True

                if not fail:
                    # Update the floors
                    __floors[floor] = old_floor
                    __floors[ne]    = new_floor
                    # Make a state to eliminate duplicates
                    new_state = (ne, str(__floors))
                    # Add new state if we haven't done this one already
                    if new_state not in states:
                        states.add(new_state)
                        #print('Pass:',ne, new_floor, floor, old_floor)
                        #print('New floors: ---',__floors)
                        new_moves = moves+1
                        if new_moves < 100:
                            q.append((moves+1,ne,__floors))
        
        
print('Part 1:', solve())
#print('Part 2:', solve(True))

