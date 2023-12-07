import sys
sys.path.append('/home/rwilkinson/Python')

from networkx import nx

G = nx.Graph()

root = "COM"
nodes = {}

with open("day06_input.txt",'r') as f:
    for line in f.readlines():
        parent, child = line.rsplit()[0].split(')')
        G.add_edge(parent, child)
        if parent != root:
            if parent not in nodes:
                nodes[parent] = 1
        if child not in nodes:
            nodes[child] = 1

direct = 0
indirect = 0

for n in nodes:
    direct   += 1
    indirect += nx.dijkstra_path_length(G,n,root) - 1

print "Part 1:"
print "Direct: {}, Indirect: {}".format(direct, indirect)
print "Total: {}".format(direct+indirect)

print "Part 2:"
src = "YOU"
dst = "SAN"
print "Transfers: {}".format(nx.dijkstra_path_length(G,src,dst)-2)
