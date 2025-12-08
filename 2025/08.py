import numpy as np

# Read the input
lines = open("08a.in").read().splitlines()

boxes = {}
circuits = []

def ed(a,b):
    'Euclidean distance'
    p1 = np.array(a)
    p2 = np.array(b)
    d = np.linalg.norm(p1 - p2)
    return d

for line in lines:
    x,y,z = [int(a) for a in line.split(',')]
    boxes[(x,y,z)] = 1

# Fid the nearest other box
for box1 in boxes:
    nearest = None
    for box2 in boxes:
        if box1 == box2: continue
        distance = ed(box1,box2)
        if nearest is None or distance < nearest[1]:
            nearest = (box2, distance)
    boxes[box1] = nearest

# Now make the circuits
num = 0
# use the shortest distances between boxes as the sort
for box, nearest in sorted(boxes.items(), key=lambda x: x[1][1]):
    print(box, nearest)
    if num < 10:
        # No circuit so make the first
        if len(circuits) == 0:
            circuits.append({box, nearest[0]})
        else:
            found = False
            for circuit in circuits:
                if not found and nearest[0] in circuit:
                    circuit.add(box)
                    found = True
            if not found: # Make a new circuit
                circuits.append({box, nearest[0]})
    else:
        circuits.append({box})
    num += 1

for a in circuits:
    print('---')
    for b in a:
        print(b)
