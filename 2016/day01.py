loc = (0,0)
curdir = 'N'

rights = {'N':'E',
          'E':'S',
          'S':'W',
          'W':'N'}

lefts = {'N':'W',
         'E':'N',
         'S':'E',
         'W':'S'}

turns = []
visited = set()
twice = None

def turn(d, cur):
    if d[0] == 'R':
        return rights[cur]
    else:
        return lefts[cur]

def move(d, l):
    x,y = l
    dist = int(d[1:])

    for i in range(dist):
        if curdir == 'N':
            y += 1
            check_visit(x,y)
        elif curdir == 'E':
            x += 1
            check_visit(x,y)
        elif curdir == 'S':
            y -= 1
            check_visit(x,y)
        elif curdir == 'W':
            x -= 1
            check_visit(x,y)

    return (x,y)

def manhattan(l):
    x,y = l
    return abs(x) + abs(y)

def check_visit(x,y):
    global twice
    intloc = (x,y)
    if intloc in visited:
        if twice is None:
            twice = intloc
    # Been there now
    visited.add(intloc)

with open("day01_input.txt") as f:
    for line in f.readlines():
        turns.extend(line.split(', '))

#turns = "R8, R4, R4, R8".split(', ')

visited.add(loc)

for t in turns:
    curdir = turn(t, curdir)
    loc = move(t, loc)

print("Part 1:", manhattan(loc))
print("Part 2:", manhattan(twice))
