import random
import networkx as nx

lines = open('25.in').read().splitlines()

G = nx.Graph()

# Make nodes
for line in lines:
    src, r = line.split(': ')
    dests = r.split(' ')
    for dest in dests:
        G.add_edge(src, dest, capacity=1)

# Use minimum cut to chop up the graph into pieces
while True:
    nodes = list(G.nodes())
    a,b = random.choices(nodes, k=2)
    if a == b: continue
    cut, partition = nx.minimum_cut(G, a, b)
    if cut == 3:
        print('Part 1:', len(partition[0]) * len(partition[1]))
        break
