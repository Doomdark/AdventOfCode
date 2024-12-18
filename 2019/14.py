lines = open('14.in').read().splitlines()

from collections import defaultdict, Counter
import math

chemicals = defaultdict()

for line in lines:
    left, right = line.split(' => ')
    lefts = [x.split() for x in left.split(', ')]
    lefts = {chem:int(num) for num,chem in lefts}
    num, chem = right.split()
    chemicals[chem] = {'num':int(num), 'sources':lefts}

def calc_ore(fuel=1):
    global chemicals

    C = Counter()
    C['FUEL'] = fuel

    last_C = None

    # Iterate until the new C doesn't change vs old C
    while last_C != C:
        # Prevent the dict changing inaide the loop
        last_C = C.copy()
        # Iterate over all the chemicals
        for right, eq_data in chemicals.items():
            # Get the units from the last iteration
            for got_unit, got_num in last_C.items():
                if got_unit == right and got_num > 0:
                    mult = math.ceil(got_num / eq_data['num'])
                    C[got_unit] -= mult * eq_data['num']

                    for left_unit, left_num in eq_data['sources'].items():
                        C[left_unit] += mult * left_num

    return C['ORE']

one_fuel = calc_ore(1)
print('Part 1:', one_fuel)

# -- Part 2 --

# Not sure how todo this so do a binary search to speed things up

# Set the initial bounds
l,r = one_fuel,one_fuel*(10**8)
# Run until l and r are different by 1
while r-l != 1:
    m = (l+r)//2
    if calc_ore(m) > 1000000000000: r = m
    else: l = m

print('Part 2:', l)
