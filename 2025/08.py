import numpy as np
import networkx.utils.union_find as uf

# Read the input
lines = open("08.in").read().splitlines()

boxes = []
dists = set()
conns = []

def ed(a,b):
    'Euclidean distance'
    p1 = np.array(a)
    p2 = np.array(b)
    d = np.linalg.norm(p1 - p2)
    return d

for line in lines:
    x,y,z = [int(a) for a in line.split(',')]
    boxes.append((x,y,z))

# Fid the nearest other box
for box1 in boxes:
    for box2 in boxes:
        if box1 == box2: continue
        distance = ed(box1,box2)
        # Don't repeat the distances. It's v unlikely they'll be duplicated.
        if distance not in dists:
            conns.append((distance, box1, box2))
            dists.add(distance)

# Sort the connections by distance
conns.sort()

# Make a list with the first 1000 connections in
closest = []
for conn in conns[:1000]:
    closest.append((conn[1],conn[2]))

# Merge the connections
ds = uf.UnionFind()
sets = []
for g in closest: ds.union(*g)
for s in ds.to_sets(): sets.append(len(s))
sets.sort()

# The biggest 3 sets need multiplying together
print('Part 1:', sets[-1]*sets[-2]*sets[-3])

# Make a list with all the connections in
closest = []
for conn in conns:
    closest.append((conn[1],conn[2]))

# Go through all of the connections and merge them until there is only 1 set
for i in range(2,len(closest)):
    sets = []
    for g in closest[:i]: ds.union(*g)
    for s in ds.to_sets(): sets.append(s)
    # Check there's only 1 set and that the set length is the same as the number of boxes
    if len(sets) == 1 and len(sets[0]) == len(lines):
        print('Part 2:', closest[i-1][0][0] * closest[i-1][1][0])
        exit(0)
