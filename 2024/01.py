lines = open("01.in").read().splitlines()

left  = []
right = []

for line in lines:
    l, r = line.split()
    left.append(int(l))
    right.append(int(r))

left  = sorted(left)
right = sorted(right)

total = 0

for l,r in zip(left,right):
    total += abs(l-r)

print('Part 1:', total)

total = 0

for l in left:
    times = right.count(l)
    total += times * l

print('Part 2:', total)
