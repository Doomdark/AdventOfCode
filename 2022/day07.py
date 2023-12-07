class Node:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.kids = []
        self.parent = None

    def get_size(self):
        size = self.size
        for kid in self.kids:
            size += kid.get_size()
        return size

    def is_dir(self):
        return self.kids != []

    def print(self,i):
        print(' '*i, "- {} ({}{})".format(self.name, 'dir' if self.is_dir() else 'file',
                                          '' if self.is_dir() else ', {}'.format(self.size)))
        for kid in self.kids:
            kid.print(i+2)

lines = open("7.in").read().split('\n')

cnode = None
# Make a root nod
root = Node('/',0)
cnode = root

nodes = []

for line in lines[1:]:
    # Command
    if line.startswith('$'):
        cmd = line.strip().split()
        if cmd[1] == 'ls':
            listing = True
        elif cmd[1] == 'cd':
            if cmd[2] == '..':
                cnode = cnode.parent
            else:
                for kid in cnode.kids:
                    if kid.name == cmd[2]:
                        cnode = kid
                        break
    elif line.strip() != '':
        l = line.strip().split()
        if l[0] == 'dir':
            name,size = l[1],0
        else:
            size,name = int(l[0]), l[1]
        node = Node(name, size)
        cnode.kids.append(node)
        node.parent = cnode
        nodes.append(node)

#root.print(0)

# Get sum of directories with <= 100000
dirs = []
for node in nodes:
    if node.is_dir():
        if node.get_size() <= 100000:
            dirs.append(node)

#print([n.name for n in dirs])
print("Part 1", sum([n.get_size() for n in dirs]))

## Part 2 ##

# Find smallest directory to delete that is >
total_size = root.get_size()
csize = 70000000 - total_size
rsize = 30000000 - csize

cur = root
for node in nodes:
    if rsize < node.get_size():
        if node.get_size() < cur.get_size():
            cur = node

print('Part 2:', cur.get_size())
