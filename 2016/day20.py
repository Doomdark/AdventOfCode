ranges = {}

with open("20.in") as f:
    for line in f.readlines():
        lo,hi = [int(x) for x in line.strip().split('-')]
        ranges[lo] = hi

def part1():
    lowest = 0
    for lo,hi in sorted(ranges.items()):
        if lo<=lowest<=hi:
            lowest = hi+1
    return lowest
    
print('Part 1:', part1())

def part2():
    current_hi = 0
    # Count of available IPs
    total = 0
    # Iterate through the sorted ranges
    for lo,hi in sorted(ranges.items()):
        # lo is above the current top of the range so add the gap in the blacklist range to the total
        if lo > current_hi+1:
            total += lo - current_hi -1
        # Store the current top of the used range
        current_hi = max(hi, current_hi)
    # Lastly, add the max value minus the final top of the range to the total
    total += (2**32)-1 - current_hi
    return total

print('Part 2:', part2())

