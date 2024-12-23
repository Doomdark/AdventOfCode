lines = open('23.in').read().splitlines()

from collections import defaultdict
from itertools import combinations

Nodes = set()
Adjacent = defaultdict(list)

for line in lines:
    l,r = line.split('-')
    Nodes.add(l)
    Nodes.add(r)
    Adjacent[r].append(l)
    Adjacent[l].append(r)

def get_connected(num=3):
    groups = set()
    for comb in combinations(Adjacent.keys(),num):
        comb0 = list(comb)
        connected = True
        # Test all keys against all
        for n in range(len(comb)):
           a = comb0[0]
           within = all([a in Adjacent[c] for c in comb0[1:]])
           if not within:
               connected = False
               break
           comb0 = comb0[1:] + [comb0[0]]
        if connected:
            groups.add(tuple(sorted(list(comb))))
    return groups

c = get_connected(3)
part1 = 0
for cc in c:
    if any([ccc.startswith('t') for ccc in cc]):
        part1 += 1
print('Part 1:', part1)

# -- Part 2 --

# Part 1 takes ages. Try something else for part 2.

# We only need the first group of any given size for part 2.

def get_connected2(nodes, remaining):
    # Ran out of connection depth so we've found a group of the required size.
    # Return an empty list to append the node tree to.
    if remaining == 0:
        return []
    # For each node in the provided list try to get the connections
    for n in nodes:
        # Get all the nodes adjacent to this node in the nodes list
        adjacent_nodes = filter(lambda x: x!=n and (x in Adjacent[n]), nodes)
        # Now do the same thing on all the adjacent nodes
        ret = get_connected2(adjacent_nodes, remaining-1)
        # If the function returned a list then add this node to the list and return it.
        # Otherwise there were no connections.
        if ret is not None:
            ret.append(n)
            return ret
    # If we got here then there are no nodes to connect to
    return None

# Try group sizes upwards from 4 as that's where we stopped in part 1
part2 = None
size = 4
while True:
    l = get_connected2(Nodes, size)
    # If we didn't find anything of that size then the previous value is the answer.
    if l is None:
        break
    # Store the current maximum
    part2 = l
    size += 1

print('Part 2:', ','.join(sorted(list(part2))))
