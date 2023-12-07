assigns = []

with open("day04_input.txt") as f:
    for line in f.readlines():
        r1,r2 = line.strip().split(',')
        r1start,r1end = [int(x) for x in r1.split('-')]
        r2start,r2end = [int(x) for x in r2.split('-')]
        r1set = set()
        r2set = set()
        for i in range(r1start,r1end+1):
            r1set.add(i)
        for i in range(r2start,r2end+1):
            r2set.add(i)
        assigns.append((r1set, r2set))

part1 = 0

for a in assigns:
    r1, r2 = a
    # Check if the intersection of sets is the same length as r1
    if len(r1.intersection(r2)) == len(r1):
        part1 += 1
        continue
    # Check if the intersection of sets is the same length as r2
    if len(r2.intersection(r1)) == len(r2):
        part1 += 1

print("Part 1:", part1)

part2 = 0

for a in assigns:
    r1, r2 = a
    # Check if the intersection of sets has at least 1 item in it
    if len(r1.intersection(r2)) > 0:
        part2 += 1

print("Part 2:", part2)
