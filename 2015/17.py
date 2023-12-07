from itertools import combinations
from collections import defaultdict

containers = []

lines = open('17.in').read().splitlines()
for line in lines:
    containers.append(int(line))

def solve(volume):
    total = 0
    min_containers = 1000
    comb_ways = defaultdict(int)
    # Iterate over each possible number of containers
    for count in range(1,len(containers)+1):
        # Get all the combinations
        combs = list(combinations(containers, count))
        # Sum each combinations and count how many add upto 150
        for comb in combs:
            # If the combination sum == required volume then increment the total
            if sum(comb) == volume:
                total += 1
                if count <= min_containers:
                    min_containers = count
                    comb_ways[count] += 1

    # How many combinations are there for the minimum number of containers?
    return total, comb_ways[min_containers]

solution = solve(150)
print('Part 1:', solution[0])
print('Part 2:', solution[1])
