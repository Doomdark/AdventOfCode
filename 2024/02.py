lines = open('02.in').read().splitlines()

lists = []

for line in lines:
    level = [int(x) for x in line.split()]
    lists.append(level)

def get_direction(report, last):
    if report - last > 0:
        return 1
    elif report - last == 0:
        return 0
    else:
        return -1

def is_inc_dec(report):
    return (sorted(set(report)) == report) or (sorted(set(report),reverse=True) == report)

def check(l):
    last = None
    direction = None

    for i,report in enumerate(l):
        # Set direction
        if i==1:
            direction = get_direction(report, last)
            if direction == 0:
                return False
        # Check for difference
        if i>0:
            diff = abs(report-last)
            if not (1 <= diff <= 3):
                return False
        # Check for all increasing/decreasing
        if i>1:
            newdir = get_direction(report, last)
            if newdir == 0 or newdir != direction:
                return False

        last = report

    return True

def part1(lists):
    return sum([check(l) for l in lists])

print('Part 1:', part1(lists))

def part2(lists):
    total = 0
    for l in lists:
        # Remove each entry in turn and check if that would make it safe
        safe = 0
        for i in range(len(l)):
            _l = l[:]
            del _l[i]
            safe += check(_l)
            if safe>0:
                break
        # If any are safe then we're good
        if safe>0: total += 1
    return total

print('Part 2:', part2(lists))
