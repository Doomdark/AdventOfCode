import itertools

left  = []
right = []

with open("13.in") as f:
    for line in f.readlines():
        if line.strip() == '':
            continue
        if len(left) == len(right):
            left.append(eval(line.strip()))
        else:
            right.append(eval(line.strip()))

part1 = 0

def compare(c,l,r):
    global part1
    done = False

    # Compare integers
    if isinstance(l,int) and isinstance(r,int):
        if l < r:
            part1 += c
            return True
        elif l == r:
            return False
        else:
            return True
    elif l is list and len(l) == 0:
        part1 += c
        return True
    elif r is list and len(r) == 0:
        return True
    elif l == '#':
        part1 += c
        return True
    elif r == '#':
        return True

    nl = l
    nr = r
    if not isinstance(l,list): nl = [l]
    if not isinstance(r,list): nr = [r]

    for ll,rr in itertools.zip_longest(nl,nr,fillvalue='#'):
        done = compare(c,ll,rr)
        if done:
            return True

    return False

c = 1

for l,r in itertools.zip_longest(left,right,fillvalue='#'):
    compare(c,l,r)
    c += 1

print('Part 1:',part1)

## Part 2 ##

# Do a compare function to sort the list
def compare (l, r):
    if type(l) is list or type(r) is list:
        if type(r) is not list: r = [r]
        if type(l) is not list: l = [l]
        for le, re in zip(l, r):
            c = compare (le, re)
            if c != 0: return c
        return len(l)-len(r)
    else:
        return l-r

# for each list item return the iterables in the right order
lines = [eval(x) for x in open("13.in").read().strip().splitlines() if x != '']
lines.append([[2]])
lines.append([[6]])

from functools import cmp_to_key

nlist = sorted(lines, key=cmp_to_key(compare))

two = nlist.index([[2]]) + 1
six = nlist.index([[6]]) + 1
#print(two,six)
print('Part 2:', two*six)
