from collections import defaultdict

lines = open('07.in').read().splitlines()

eqs = defaultdict(list)

for line in lines:
    l,r = line.split(':')
    _r = [int(x) for x in r.split()]
    eqs[int(l)].append(_r)

def dec_operators(val,ops):
    # First non-zero value
    fnz = 0
    for n in range(len(val)):
        if val[n] > 0:
            fnz = n
            break
    # Now decrement the operators
    nval = val[:]
    for n in range(len(val)):
        if n<fnz:
            nval[n] = ops
        elif n==fnz:
            nval[n] = val[n]-1
    return nval

def solve(val, nums, part2=False):
    total = 0
    good = False
    # Make a list of operators
    ops = 3 if part2 else 2
    operators = [ops-1]*(len(nums)-1)
    # Do the maths
    while(not good):
        # Start with the first number
        SUM = nums[0]
        # Apply the operators with the other numbers
        for n in range(1,len(nums)):
            operator = operators[n-1]
            # Try a mul first
            if not part2:
                if operator == 1:
                    SUM *= nums[n]
                else:
                    SUM += nums[n]
            else: # part 2
                if  operator == 2:
                    SUM = int(''.join([str(SUM), str(nums[n])]))
                elif operator == 1:
                    SUM *= nums[n]
                else:
                    SUM += nums[n]
            if SUM > val:
                break
        if SUM == val:
            good = True
            break
        if any([x>0 for x in operators]):
            operators = dec_operators(operators,ops-1)
        else:
            break
    return val if good else 0

def dfs(val, items, part2=False):
    if items[0] > val:
        return False
    if len(items) == 1:
        return val == items[0]
    if dfs(val, [items[0]+items[1]] + items[2:], part2):
        return True
    if dfs(val, [items[0]*items[1]] + items[2:], part2):
        return True
    if part2:
        if dfs(val, [int(''.join([str(items[0]), str(items[1])]))] + items[2:], part2):
            return True
    return False

def solve2(part2=False):
    total = 0
    for val, nums_list in eqs.items():
        for nums in nums_list:
            if dfs(val, nums, part2):
            #if solve(val, nums, part2):
                total += val
    return total

print('Part 1:', solve2())
print('Part 2:', solve2(True))
