# Read the input
lines = open("05.in").read().splitlines()

ranges = set()
ingredients = set()

for line in lines:
    if '-' in line:
        l,r = [int(x) for x in line.split('-')]
        ranges.add((l,r))
    elif line:
        ingredients.add(int(line))

fresh = set()
for i in ingredients:
    for l,r in ranges:
        if l<=i<=r:
            fresh.add(i)

print('Part 1:', len(fresh))

overlapped_ranges = set()

def get_overlapping_ranges(R1,R2):
    newr = set()
    l1,r1 = R1
    l2,r2 = R2

    # Always add the new range
    newr.add(R1)

    if l1 < l2:
        if r1 < l2:
            # R1 is wholly left of R2
            newr.add(R2)
        else: # r1 >= l2
            # R1 inside R2
            if r1 < r2:
                # Add trimmed R2 RHS
                newr.add((r1+1,r2))
    elif l1 == l2:
        if r1 < r2:
            # Add trimmed R2 RHS
            newr.add((r1+1,r2))
    else: # l1 > l2
        if l1 > r2:
            # R1 is wholly right of R2
            newr.add(R2)
        elif l1 == r2:
            newr.add((l2,r2-1))
        else: # l1 < r2
            # R2 covers R1 entirely
            if r1 <= r2:
                newr.add((l2,l1-1))
                newr.add((r1+1,r2))
            else:
                newr.add((l2,l1-1))

    return newr

for l,r in ranges:
    skip = False
    new_ranges = set()
    # Any existing ranges?
    if not overlapped_ranges:
        overlapped_ranges.add((l,r))
    else:
        for L,R in overlapped_ranges:
            new_ranges.update(get_overlapping_ranges((l,r),(L,R)))
            overlapped_ranges = new_ranges

total = 0
for l,r in overlapped_ranges:
    total += r-l+1

print('Part 2:', total)
