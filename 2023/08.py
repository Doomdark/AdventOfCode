import itertools, re
import math
from collections import defaultdict
from functools import reduce

lines = open('08.in').read().splitlines()

nodes = defaultdict()

for line in lines:
    if '=' in line:
        n, l, r = re.findall('[A-Z0-9]+', line)
        nodes[n] = {'L':l, 'R':r}
    elif line != '':
        directions = str(line)

# Part 1

# Starting node
node = 'AAA'

# Starting instruction and step count
inst = 0
steps = 0

def move(node):
    global steps, inst, nodes, directions
    steps += 1
    newnode = nodes[node][directions[inst]]
    # Move on inst
    inst = (inst + 1) % len(directions)
    return newnode

# Move until we get to ZZZ
while node != 'ZZZ':
    node = move(node)

print('Part 1:', steps)

# Part 2

step_counts = []

parallel_nodes = [x for x in nodes.keys() if x.endswith('A')]

def move_all(node):
    global steps, inst
    inst  = 0
    steps = 0
    while not node.endswith('Z'):
        node = move(node)
    return steps

# Move all the nodes until they hit a node ending in Z
for node in parallel_nodes:
    # Accumulate the step counts for each node
    step_counts.append(move_all(node))

# Least common multiple for an array
def lcm(arr):
    l = reduce(lambda x,y:(x*y)//math.gcd(x,y),arr)
    return l

# Least common multiple of all step counts to get the answer
print('Part 2:', lcm(step_counts))
