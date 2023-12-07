timestamp = 0
times = []

with open("Day13_input.txt") as f:
    timestamp = int(f.readline().rstrip())
    times = [int(x) for x in f.readline().rstrip().split(',') if x != 'x']

times.sort()

def part1():
    for c,i in enumerate(range(timestamp, timestamp+max(times))):
        for j in times:
            if i%j == 0:
                print ("Part 1:", j*c)
                return

part1()

with open("Day13_input.txt") as f:
    timestamp = f.readline() # Don't care about this for part 2
    # Add the list position in the tuple
    times = [(c,int(x)) for c,x in enumerate(f.readline().rstrip().split(',')) if x!='x' ]

import math

# Least common multiple
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

matched = {}

def part2():
    # Start at the smallest possible non-zero time
    time = min([x[1] for x in times])
    # Increment by the smallest multiple initially
    increment = min([x[1] for x in times])
    # Run until we get the answer
    while(1):
        # Default to found
        found = True
        for c,i in times:
            # A match is when the current time plus the position is divisible by the bus time
            if (time+c)%i != 0:
                # No match - break out of this checking loop and go on to the next time increment
                found = False
                break
            # Found a match so increase the increment to be the least common multiple so far
            elif i not in matched:
                #print ("GCD of", increment, i, "=", math.gcd(increment, i))
                increment = lcm(increment, i)
                matched[i] = 1
        # Found the answer
        if found:
            print ("Part 2:", time)
            return
        # Increase the time by the current least common increment value
        time += increment

part2()

