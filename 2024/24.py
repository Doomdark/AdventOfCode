from collections import defaultdict
import copy
import graphviz

class Gate:
    def __init__(self,a,b,z,aw,bw,zw):
        self.a = a
        self.b = b
        self.z = z
        self.aw = aw
        self.bw = bw
        self.zw = zw
        self.changed = False

    def run(self):
        if self.a is None or self.b is None:
            return
        _z = self.z
        self.op()
        self.changed = False
        if (_z is None and self.z is not None) or (_z != self.z):
            self.changed = True
        if self.changed:
            for gate in gates:
                if self.zw == gate.aw: gate.set_a(self.z)
                if self.zw == gate.bw: gate.set_b(self.z)

    def set_a(self,val):
        self.a = val

    def set_b(self,val):
        self.b = val

    def __str__(self):
        return ' '.join([self.aw, self.OP, self.bw, '->', self.zw, str(self.a), str(self.b), str(self.z)])

class AND(Gate):
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '&'
    def op(self):
        self.z = self.a & self.b

class OR(Gate):
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '|'
    def op(self):
        self.z = self.a | self.b

class XOR(Gate):
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '^'
    def op(self):
        self.z = self.a ^ self.b

def init(filename='24.in', do_graph=False, problem_bit=0):
    lines = open(filename).read().splitlines()
    wires = defaultdict()
    gates = []

    for line in lines:
        if ':' in line:
            wire, initial = line.split(': ')
            wires[wire] = int(initial)
        elif '->' in line:
            aw, op, bw, eq, zw = line.split()
            a = wires.get(aw, None)
            b = wires.get(bw, None)
            z = wires.get(zw, None)
            g = None
            if   op == 'AND': g = AND(a,b,z,aw,bw,zw)
            elif op == 'OR' : g = OR(a,b,z,aw,bw,zw)
            elif op == 'XOR': g = XOR(a,b,z,aw,bw,zw)
            gates.append(g)

    return wires, gates

# Simulate until all the zXX wires have a value
def simulate(gates):
    while True:
        changed = False
        for gate in gates:
            gate.run()
            if gate.changed:
                changed = True
        if not changed:
            return gates

# Get all the z wire values:
wires, gates = init()
part1 = ''
g = simulate(gates)
outputs = {x.zw:str(x.z) for x in g if x.zw.startswith('z')}
for name, value in sorted(outputs.items(), reverse=True):
    part1 += value

print('Part 1:', int(part1,2))

# -- Part 2 --

# This doesn't do the right thing yet...
def make_digraph(bit):
    graph = graphviz.Digraph("24")
    for gate in gates:
        graph.edge(gate.aw, gate.zw, f'{gate.OP} {gate.z}')
    graph.node(bit, bit, style='filled', fillcolor='red')
    graph.render()

# Modify part 2's input when we determine the bits that are incorrect.
# Start with the LSBs and work upwards

#  Re-run part 1 with the modified input
wires, gates = init('24.in')
part1 = ''
g = simulate(gates)
outputs = {x.zw:str(x.z) for x in g if x.zw.startswith('z')}
for name, value in sorted(outputs.items(), reverse=True):
    part1 += value
actual = f'0b{part1}'

# Print out the expected values
x,y = '',''
for name, value in sorted(wires.items(), reverse=True):
    if name.startswith('x'): x += str(value)
    if name.startswith('y'): y += str(value)
expected = bin(int(x,2) + int(y,2))

# Which bits in the output are wrong?
print('ACTUAL', actual)
print('EXPECT', expected)

j = 0
for i in range(len(expected[2:])-1,0,-1):
    if actual[i] != expected[i]:
        print(f'Bit {j} differs')
        # Make a digraph of the design now
        # I used someone else's digraph generator to solve the problwm.
        # Add a generator here when there's more time.
        #make_digraph('z{:02d}'.format(j))
        exit()
    j += 1

print('MATCH')
