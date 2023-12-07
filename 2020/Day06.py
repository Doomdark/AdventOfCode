groups = []
alls = []

with open("Day06_input.txt") as f:
    group = {}
    people = 0
    for line in f.readlines():
        if line.rstrip() != '':
            people += 1
            for char in line.rstrip():
                if char not in group:
                    group[char] = 1
                else:
                    group[char] += 1
        else:
            groups.append(group)
            alls.append(people)
            group = {}
            people = 0

print "Part 1:", sum([len(x) for x in groups])

total = 0
for p,group in zip(alls,groups):
    for v in group.itervalues():
        if v == p:
            total += 1

print "Part 2:", total
