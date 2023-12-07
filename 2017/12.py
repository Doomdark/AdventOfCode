ids = {}

# Read in initial file
with open('12.in') as f:
    for line in f.readlines():
        _id, conns = line.rstrip().split(' <-> ')
        _conns = [int(x) for x in conns.split(', ')]
        ids[int(_id)] = set(_conns)

def solve(id):
    
    group = set()
    group.add(0)
    group.update(ids[id])
    
    while(True):
        add = set()
        for i in ids:
            if i in group:
                for j in ids[i]:
                    if j not in group:
                        add.add(j)

        if add == set():
            break
        else:
            group.update(add)

    return(group)

print('Part 1:', len(solve(0)))

# Find the number of groups
members = set()
group_count = 0

while len(members) < len(ids.keys()):
    # First id not in the members list
    for i in ids.keys():
        if i not in members:
            group = solve(i)
            members.update(group)
            group_count += 1

print('Part 2:', group_count)
