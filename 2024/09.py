layout = open('09test.in').read().strip()

from collections import defaultdict

used = defaultdict()
free = set()
ids = defaultdict()
gaps = defaultdict()

ID = 0
loc = 0
free_id = 0
for n,char in enumerate(layout):
    num = int(char)
    # file
    if n%2 == 0:
        for i in range(num):
            used[loc+i] = ID
        ids[ID] = (loc,num)
        ID += 1
    else:
        for i in range(num):
            free.add(loc+i)
        gaps[free_id] = (loc,num)
        free_id += 1
    loc += num

# Move the rightmost things to the left
import copy
free_orig = copy.copy(free)
used_orig = copy.copy(used)

while (len(free)>0):
    gap = min(free)
    mover = max(used.keys())
    if gap > mover:
        break
    used[gap] = used[mover]
    del used[mover]
    free.remove(gap)

def p(thing):
    l = ''
    m = max(thing.keys())
    for i in range(m+1):
        if i in thing.keys():
            l += '{}'.format(thing[i])
        else:
            l += '.'
    print(l)

p(used)
total = sum([x*y for x,y in used.items()])
print('Part 1:', total)

def move(used,src,dst,length):
    for i in range(length):
        used[dst+i] = used[src+i]
        del used[src+i]
    return used

used = used_orig
p(used)
free = free_orig
move_id = max(ids.keys())
while (move_id >= 0):
    mloc,mnum = ids[move_id]
    newgaps = copy.copy(gaps)
    for fid,val in sorted(gaps.items()):
        gloc,gnum = val
        # If the file fits then move it
        if gloc > mloc:
            break
        if gnum >= mnum:
            # Move the real file in the layout
            used = move(used,mloc,gloc,mnum)
            # Update the free space map
            ngnum = gnum-mnum
            ngloc = gloc+mnum
            if ngnum > 0:
                newgaps[fid] = (ngloc,ngnum)
            break
    gaps = newgaps
    move_id -= 1

p(used)
total = sum([x*y for x,y in used.items()])
print('Part 2:', total)
