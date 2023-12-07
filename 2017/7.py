import sys

class Disc:
    def __init__(self, weight, children):
        self.weight = weight
        self.children = children
        self.parent = None

    def get_weight(self):
        weight = self.weight
        for child in self.children:
            weight += discs[child].get_weight()
        return weight

    def check_weight(self):
        # Check all child weights are the same
        weights = [discs[x].get_weight() for x in self.children]
        if len(set(weights)) > 1:
            print("Weights differ:", self.children)
            for child in self.children:
                print(discs[child].get_weight(), discs[child].weight)
            sys.exit(1)

discs = {}

with open("7.in") as f:
    for line in f.readlines():
        #print(line)
        l = line.strip().split('->')
        l1 = l[0].split()
        node = l1[0]
        weight = int(l1[1].replace('(','').replace(')',''))
        children = []
        #print(l)
        if len(l) > 1:
            l2 = [x.strip() for x in l[1].split(', ')]
            children = l2

        disc = Disc(weight, children)
        #print(node, num, children)
        discs[node] = disc

# Assign parents
for k,v in discs.items():
    if v.children:
        for child in v.children:
            discs[child].parent = k

# Which disc has no parent?
for k,v in discs.items():
    if v.parent is None:
        print('Part 1:', k)
        break

for k,v in discs.items():
    v.check_weight()
