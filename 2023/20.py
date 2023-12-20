lines = open('20.in').read().splitlines()

from collections import deque

components = {}
update_queue = deque()
all_conjunctions = []

low_pulses = 0
high_pulses = 0

verbose = False

def update_low_pulses():
    global low_pulses
    low_pulses += 1

def update_high_pulses():
    global high_pulses
    high_pulses += 1

class Base:
    def __init__(self, name, dests, update_queue):
        self.name = name
        self.val = 0
        self.dests = dests
        self.queue = deque()
        self.update_queue = update_queue

    def __repr__(self):
        return '{} {} {}'.format(self.name, self.val, self.dests)
        
class Conjunction(Base):
    'NAND gate'
    def __init__(self, name, dests, update_queue):
        Base.__init__(self,name, dests, update_queue)
        self.memory = {}

    def add_src(self, name):
        self.memory[name] = 0

    def update(self):
        src, pulse = self.queue.popleft()
        self.memory[src] = pulse
        all_1 = all([x for x in self.memory.values()])
        for dest in self.dests:
            send_pulse = 0 if all_1 else 1
            if verbose: print(self.name, send_pulse, '->', dest)
            components[dest].queue.append((self.name, send_pulse))
            self.update_queue.append(dest)
            if send_pulse == 0: update_low_pulses()
            else:               update_high_pulses()
        
class Flop(Base):
    'Toggle flip-flop'
    def __init__(self, name, dests, update_queue):
        Base.__init__(self, name, dests, update_queue)

    def update(self):
        src, pulse = self.queue.popleft()
        if pulse == 0:
            self.val = 0 if self.val else 1
            for dest in self.dests:
                if verbose: print(self.name, self.val, '->', dest)
                components[dest].queue.append((self.name, self.val))
                self.update_queue.append(dest)
                if self.val == 0: update_low_pulses()
                else:             update_high_pulses()
      
class Broadcast(Base):
    'Broadcaster guy'
    def __init__(self, name, dests, update_queue):
        Base.__init__(self, name, dests, update_queue)

    def update(self):
        src, pulse = self.queue.popleft()
        if pulse == 0:
            for dest in self.dests:
                if verbose: print(self.name, 0, '->', dest)
                components[dest].queue.append((self.name,0))
                self.update_queue.append(dest)
                update_low_pulses()

class Button(Base):
    'Button to press'
    def __init__(self, name, dests, update_queue):
        Base.__init__(self, name, dests, update_queue)

    def push(self):
        'Send a low pulse to each destination.'
        for dest in self.dests:
            if verbose: print(self.name, 0, '->', dest)
            components[dest].queue.append((self.name,0))
            self.update_queue.append(dest)
            update_low_pulses()

class Debug(Base):
    'Debug receiver'
    def __init__(self, name, dests, update_queue):
        Base.__init__(self, name, dests, update_queue)

    def update(self):
        src, pulse = self.queue.popleft()

# Parse the lines
for line in lines:
    name, dests = line.split(' -> ')
    _dests = dests.split(', ')
    _name = name[1:]
    if name.startswith('&'):
        components[_name] = Conjunction(_name, _dests, update_queue)
        all_conjunctions.append(_name)
    elif name.startswith('%'):
        components[_name] = Flop(_name, _dests, update_queue)
    else:
        components[name] = Broadcast(name, _dests, update_queue)

# Add a button
button = Button('button', ['broadcaster'], update_queue)

# Link the conjunction sources to each conjunction
debug_components = {}
for component in components.values():
    for dest in component.dests:
        # If this destination is not in the components list then it's for debug
        if dest not in components.keys():
            if dest not in debug_components:
                debug = Debug(dest, [], update_queue)
                debug_components[dest] = debug
        # Ifthis is a conjunction then add it as a source to the appropriate conjunction
        if dest in all_conjunctions:
            components[dest].add_src(component.name)

# Merge the debug components dictionary with the regular components
components = components | debug_components

def solve(pushes=1):
    global update_queue, high_pulses, low_pulses
    low_pulses = 0
    high_pulses = 0

    for _ in range(pushes):
        button.push()
        
        # Run until the updates stop
        while update_queue:
            # Do the items currently in the queue
            for i in range(len(update_queue)):
                component = update_queue.popleft()
                components[component].update()

    return high_pulses * low_pulses

print('Part 1:', solve(1000))

# Part 2

# Construct a graphviz digraph of all the elements to visualise the logic

flops     = []
ands      = []
inverters = []
other     = []

digraph = open('20.dot', 'wt')
digraph.write('digraph G {')

for line in lines:
    name, dests = line.split(' -> ')
    _dests = dests.split(', ')
    _name = name[1:]
    if line.startswith('&'):
        if len(_dests) == 1:
            inverters.append(_name)
        else:
            ands.append(_name)
        digraph.write(line[1:]+'\n')
    elif name.startswith('%'):
        flops.append(_name)
        digraph.write(line[1:]+'\n')        
    else:
        other.append(name)
        digraph.write(line+'\n')       

for item in flops     : digraph.write(f'{item} [style=filled, fillcolor=red]\n')
for item in ands      : digraph.write(f'{item} [style=filled, fillcolor=orange]\n')
for item in inverters : digraph.write(f'{item} [style=filled, fillcolor=yellow]\n')
for item in other     : digraph.write(f'{item} [style=filled, fillcolor=green]\n')

digraph.write('}\n')
digraph.close()

#
# Produce picture of digraph by doing this:
# dot 20.dot -Tpng -o 20.png
#
# There are 4 counters of 12 flops each.
# Each counter generates a pulse for a specific value.
# The pulses are all ANDed together before reaching the final 4-input NAND gate.
# Figure out the counters and at which count value a pulse is generated.
# The answer is then the LCM of those 4 values.
#
# Chains are in reverse order of lsb -> msb.
#
# Flops that have an arrow *towards* the associated AND gate are 1, others are 0.
#
# Chain 1: nk, nn, xf, qr, zt, pb, kq, tl, bn, sv, dx, tz
#          1   1   0   1   1   0   1   0   1   1   1   1 = 0xf5b = 3931
# Chain 2: sr, vs, tq, jm, kp, vk, tk, sh, zk, ps, qz, kh
#          1   1   0   1   0   0   0   0   1   1   1   1 = 0xf0b = 3851
# Chain 3: tp, lx, ff, df, nv, xm, cq, mq, pr, pf, nt, gs
#          1   1   1   0   0   1   1   0   1   1   1   1 = 0xf67 = 3943
# Chain 4: sj, kj, fk, xh, zs, ct, rt, hq, bb, kf, ph, hx
#          1   0   0   1   0   1   0   0   1   1   1   1 = 0xf29 = 3881
#

# Chain lengths
chain1 = 3931
chain2 = 3851
chain3 = 3943
chain4 = 3881

# Least common multiple for an array
import math
from functools import reduce

def lcm(arr):
    l = reduce(lambda x,y:(x*y)//math.gcd(x,y),arr)
    return l

array = [chain1, chain2, chain3, chain4]

print('Part 2:', lcm(array))
