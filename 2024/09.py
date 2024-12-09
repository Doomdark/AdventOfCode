layout = open('09.in').read().strip()

import copy

LIST = []
ID   = 0

for n,char in enumerate(layout):
    num = int(char)
    # File
    if n%2 == 0:
        for i in range(num):
            LIST.append(ID)
        ID += 1
    else: # Gap
        for i in range(num):
            LIST.append('.')

def get_frees(LIST):
    return iter([c for c,x in enumerate(LIST) if x == '.' ])

def get_useds(LIST):
    return iter(reversed([c for c,x in enumerate(LIST) if x != '.' ]))

frees = get_frees(LIST)
useds = get_useds(LIST)
last_used = None

while True:
    next_free = next(frees)
    next_used = next(useds)
    if next_free > next_used:
        break
    else:
        LIST[next_free] = LIST[next_used]
    last_used = next_used

total = sum([x*y for x,y in enumerate(LIST[:last_used])])
print('Part 1:', total)

# -- Part 2 --

used = {}
ids  = {}
gaps = {}
ID  = 0
loc = 0

for n,char in enumerate(layout):
    num = int(char)
    # File
    if n%2 == 0:
        for i in range(num):
            used[loc+i] = ID
        ids[ID] = (loc,num)
        ID += 1
    else: # Gap
        gaps[loc] = num
    loc += num

def p(thing):
    l = ''
    m = max(thing.keys())
    for i in range(m+1):
        if i in thing.keys():
            l += '{}'.format(thing[i])
        else:
            l += '.'
    print(l)

def move(used,src,dst,length):
    for i in range(length):
        used[dst+i] = used[src+i]
        del used[src+i]
    return used

move_id = max(ids.keys())
while (move_id >= 0):
    mloc,mnum = ids[move_id]
    newgaps = copy.copy(gaps)
    for gloc,gnum in sorted(gaps.items()):
        # If the file fits then move it
        if gloc >= mloc:
            break
        if gnum >= mnum:
            # Move the real file in the layout
            used = move(used,mloc,gloc,mnum)
            # Update the free space map
            ngnum = gnum-mnum
            ngloc = gloc+mnum
            if ngnum > 0:
                newgaps[ngloc] = ngnum
            del newgaps[gloc]
            break
    gaps = newgaps
    move_id -= 1

total = sum([x*y for x,y in used.items()])
print('Part 2:', total)
