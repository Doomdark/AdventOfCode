import graphviz

class Gate:
    'Base gate functions.'
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
    'AND gate operation'
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '&'
    def op(self):
        self.z = self.a & self.b

class OR(Gate):
    'OR gate operation'
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '|'
    def op(self):
        self.z = self.a | self.b

class XOR(Gate):
    'XOR gate operation'
    def __init__(self, a,b,z,aw,bw,zw):
        Gate.__init__(self,a,b,z,aw,bw,zw)
        self.OP = '^'
    def op(self):
        self.z = self.a ^ self.b

def init(filename='24.in'):
    'Read the input file and construct wires and gates data structures.'
    lines = open(filename).read().splitlines()
    wires = {}
    gates = []

    for line in lines:
        # First second is x and y initial values
        if ':' in line:
            wire, initial = line.split(': ')
            wires[wire] = int(initial)
        # Second section is the logic gates
        elif '->' in line:
            aw, op, bw, eq, zw = line.split()
            a = wires.get(aw, None)
            b = wires.get(bw, None)
            z = wires.get(zw, None)
            g = None
            if   op == 'AND': g = AND(a,b,z,aw,bw,zw)
            elif op == 'OR' : g = OR (a,b,z,aw,bw,zw)
            elif op == 'XOR': g = XOR(a,b,z,aw,bw,zw)
            gates.append(g)

    return wires, gates

def simulate(gates):
    'Simulate the gates until they stop changing.'
    while True:
        changed = False
        for gate in gates:
            gate.run()
            if gate.changed:
                changed = True
        if not changed:
            return gates

def evaluate(wires, gates):
    'Calculate the z output using the given gates.'
    g = simulate(gates)
    # Work out the z value by sorting the wires int the correct bit order: z00,z01,z02,etc., but then reverse them to get the real value.
    answer = ''
    outputs = {x.zw:str(x.z) for x in g if x.zw.startswith('z')}
    for name, value in sorted(outputs.items(), reverse=True):
        answer += value
    return answer

# Run part 1
wires, gates = init()
print('Part 1:', int(evaluate(wires, gates), 2) )

# -- Part 2 --

# Modify part 2's input when we determine the bits that are incorrect.
# Start with the LSBs and work upwards

# Run the simulation with a modified input including the swaps to date to get the circuit's answer.
wires, gates = init('24part2.in')
actual = evaluate(wires, gates)

# Calculate the expected answer given the x and y inputs
x,y = '',''
for name, value in sorted(wires.items(), reverse=True):
    if name.startswith('x'): x += str(value)
    if name.startswith('y'): y += str(value)
expected = bin(int(x,2) + int(y,2))[2:]

# Which bits in the output are wrong?
#print('ACTUAL', actual)
#print('EXPECT', expected)

# Make a digraph to display the circuit. Highlight the bit in error in red.
# Alter the input once you've worked out which two wire swaps cause that bit to be wrong.
# In the end I had to change the input values because I only had 3 differences for my x
# and y input values. The expected and actual values matched after I had fixed only 3 pairs
# of wires using my original x and y values.
def make_digraph(bit):
    graph = graphviz.Digraph("24")
    for gate in gates:
        graph.edge(gate.aw, gate.zw, f'{gate.OP} {gate.a}')
        graph.edge(gate.bw, gate.zw, f'{gate.OP} {gate.b}')
    graph.node(bit, bit, style='filled', fillcolor='red')
    graph.render()

# Which bit is the LSB in error?
j = 0
for i in range(len(expected)-1,0,-1):
    if actual[i] != expected[i]:
        print(f'Bit {j} differs')
        # Make a digraph of the broken design to analyse
        make_digraph(f'z{j:02d}')
        exit()
    j += 1

# These are the wire swaps I had to do to get the right answer
diffs = ['z21', 'shh', # bit 21
         'vgs', 'dtk', # bit 26
         'z33', 'dqr', # bit 33
         'pfw', 'z39'] # bit 39

print('Part 2:', ','.join(sorted(diffs)))
