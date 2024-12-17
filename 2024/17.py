lines = open('17.in').read().splitlines()

A,B,C,P,PC,output = 0,0,0,None,0,[]

for line in lines:
    if   line.startswith('Register A:'): A = int(line.split(': ')[1])
    elif line.startswith('Register B:'): B = int(line.split(': ')[1])
    elif line.startswith('Register C:'): C = int(line.split(': ')[1])
    elif line.startswith('Program:'):    P = [int(a) for a in line.split(': ')[1].split(',')]

# Run until the PC jumps outside the length of the program
while PC < len(P):
    # Next instruction
    I,O = P[PC],P[PC+1]
    # Combo operand
    CO = O
    if   O == 4: CO = A
    elif O == 5: CO = B
    elif O == 6: CO = C
    elif O == 7: raise
    # Instructions
    if I == 0: # adv
        d = 2**CO
        A = A // d
        PC += 2
    elif I == 1: # bxl
        B = B ^ O
        PC += 2
    elif I == 2: # bst
        B = CO % 8
        PC += 2
    elif I == 3: # jnz
        if A == 0: PC += 2
        else: PC = O
    elif I == 4: # bxc
        B = B ^ C
        PC += 2
    elif I == 5: # out
        o = CO % 8
        output.append(o)
        PC += 2
    elif I == 6: # bdv
        d = 2**CO
        B = A // d
        PC += 2
    elif I == 7: # cdv
        d = 2**CO
        C = A // d
        PC += 2

print('Part 1:', ','.join([str(x) for x in output]))

# The program loop looks like this:
# 2,4, B = A % 8
# 1,5, B = B ^ 5
# 7,5, C = A >> B
# 4,5, B = B ^ C
# 0,3, A = A >> 3
# 1,6, B = B ^ 6
# 5,5, output B
# 3,0  PC = 0
# So it's only testing for a 3-bit A on each iteration.
# Shove this program into z3 and get it to solve for when the B output matches each program value.
# B and C are dependent on the 3 LSBs of A.

from z3 import Optimize, BitVec

opt = Optimize()
s = BitVec('s',64)
a,b,c = s,0,0
for x in P:
    b = a % 8
    b = b ^ 5
    c = a >> b
    b = b ^ c
    a = a >> 3
    b = b ^ 6
    # Add the output constraint. b&8 must equal x.
    opt.add((b%8) == x)
# Find the smallest solution for s
opt.minimize(s)
# Run the optimizer
opt.check()
# Get the result
print('Part 2:', opt.model().eval(s))
