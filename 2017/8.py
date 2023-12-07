from collections import defaultdict

regs = defaultdict(int)

lines = open('8.in').read().splitlines()

highest = 0

for line in lines:
    l = line.split(' if ')
    dst,op,val = l[0].split()
    val = int(val)
    eSrc,eOp,eVal = l[1].split()
    expr = "regs['{}'] {} {}".format(eSrc,eOp,eVal)
    if eval(expr):
        if   op == 'inc': regs[dst] += val
        elif op == 'dec': regs[dst] -= val
    highest = max(highest,max(regs.values()))

print('Part 1:', max(regs.values()))
print('Part 2:', highest)
