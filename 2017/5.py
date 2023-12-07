offsets = [0,3,0,1,-3]

offsets = []

with open('5.in') as f:
    for line in f.readlines():
        offsets.append(int(line.strip()))

o = 0
steps = 0
while True:
    try:
        no = o + offsets[o]
        offsets[o] += 1
        o = no
        steps += 1
    except:
        print('Part 1:', steps)
        break

offsets = []

with open('5.in') as f:
    for line in f.readlines():
        offsets.append(int(line.strip()))

o = 0
steps = 0
while True:
    try:
        no = o + offsets[o]
        if offsets[o] >= 3:
            offsets[o] -= 1
        else:
            offsets[o] += 1
        o = no
        steps += 1
    except:
        print('Part 2:', steps)
        break
