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

Paths = set()

def get_connected(nodes, depth, max_depth, path, part2=False):
    # Ran out of connection depth so we've found a group of the required size.
    if depth == max_depth:
        if part2:
            # Return an empty list to append the node tree to.
            return []
        else:
            # Add the accumulated sorted path to the set of paths
            Paths.add(tuple(sorted(list(path))))
            return

    # For each node in the provided list try to get the connections
    for n in nodes:
        # Get all the nodes adjacent to this node in the nodes list
        adjacent_nodes = [x for x in nodes if x!=n and (x in Adjacent[n])]
        # Use an iterator for part 2 as it only returns one item at a time so the
        # end of the tree is reached really fast as we only care how deep it is.
        if part2:
            adjacent_nodes = iter(adjacent_nodes)
        # Now find the connectivity on all the nodes in the adjacent list
        ret = get_connected(adjacent_nodes, depth+1, max_depth, path + [n], part2)
        # For part 2, if the function returned a list then add this node to the list and return it.
        # Otherwise there were no connections.
        if part2:
            if ret is not None:
                ret.append(n)
                return ret

    # If we got here then there are no nodes to connect to
    return

# Get all the connected nodes of groups of 3
get_connected(list(Nodes), 0, 3, [])

part1 = 0
for p in Paths:
    # Check each computer in turn that it starts with a 't'
    if any([pp.startswith('t') for pp in p]):
        part1 += 1
print('Part 1:', part1)

# -- Part 2 --

# We only need the first group of any given size for part 2.

# Try group sizes upwards from 4 as that's +1 where we stopped in part 1
part2 = None
size = 4
while True:
    l = get_connected(list(Nodes), 0, size, [], True)
    # If we didn't find anything of that size then the previous value is the answer.
    if l is None:
        break
    # Store the current maximum
    part2 = l
    size += 1

print('Part 2:', ','.join(sorted(list(part2))))
