lines = open('13.in').read().splitlines()

import re

# This can be solved with Cramer's Rule. I had to look it up.
# https://en.wikipedia.org/wiki/Cramer%27s_rule

def determinant(a, b):
    return a[0]*b[1] - a[1]*b[0]

def coords(a, b, p):
    d = determinant(a,b)
    n = determinant(p,b)
    m = determinant(a,p)
    if n%d==0 and m%d==0:
        return (n//d, m//d)
    return None
    
def solve(adder):
    a,b,p = 0,0,0
    total = 0
    for line in lines:
        if not line: continue
        match = re.match('.*(A|B|Prize): X[+=](\d+), Y[+=](\d+)', line)
        if match:
            v = (int(match.group(2)), (int(match.group(3))))
            if match.group(1) == 'A': a = v
            if match.group(1) == 'B': b = v
            if match.group(1) == 'Prize':
                p = (v[0]+adder, v[1]+adder)
                c = coords(a, b, p)
                if c:
                    total += c[0]*3 + c[1]
    return total

print('Part 1:', solve(0))
print('Part 2:', solve(10000000000000))
