lines = open('13test.in').read().splitlines()

import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

class Machine:
    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize

    def part1(self):
        min_x = min(self.a[0], self.b[0])
        min_y = min(self.a[1], self.b[1])
        wins = []
        for a in range(self.prize[0]//min_x):
            for b in  range(self.prize[1]//min_y):
                x = a * self.a[0] + b * self.b[0]
                y = a * self.a[1] + b * self.b[1]
                if (x,y) == self.prize:
                    wins.append((a,b))
        # Which is the cheapest win?
        cheapest = None
        for a,b in wins:
            cost = a*3 + b
            if cheapest is None:
                cheapest = cost
            elif cost < cheapest:
                cheapest = cost
        return cheapest or 0

    def part2(self):
        A = ((self.prize[1]*self.a[0] - self.prize[0]*self.a[1])/
             (self.a[0]*self.b[1] - self.a[1]*self.b[0]))
        B = ((self.prize[0]*self.b[1] - self.prize[1]*self.b[0])/
             (self.a[0]*self.b[1] - self.a[1]*self.b[0]))
        if A == int(A) and B == int(B):
            return A*3 + B
        else:
            return 0

    def __str__(self):
        return ', '.join([str(self.a), str(self.b), str(self.prize)])

machines = []
adder = 0

def init(adder):
    a,b,p = 0,0,0
    for line in lines:
        if not line: continue
        l,r = line.split(": ")
        if 'A' in l:
            rr = r.split(', ')
            a = tuple([int(x[2:]) for x in rr])
        if 'B' in l:
            rr = r.split(', ')
            b = tuple([int(x[2:]) for x in rr])
        if 'Prize' in l:
            rr = r.split(', ')
            p = tuple([int(x[2:]) + adder for x in rr])
            m = Machine(a, b, p)
            machines.append(m)
            a,b,p = 0,0,0

# total = 0
# for m in machines:
#     total += m.part1()
# print('Part1:', total)

adder = 10000000000000
adder = 0
total = 0
machines = []

init(adder)
for m in machines:
    print(m)
    total += m.part2()
print('Part2:', total)
