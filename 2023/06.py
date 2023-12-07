import math

lines = open('06.in').read().splitlines()

times     = [int(x) for x in lines[0].split()[1:]]
distances = [int(x) for x in lines[1].split()[1:]]

def solve():
    results = []

    # There are n races
    for i in range(len(times)):
        wins = 0
        for speed in range(1, times[i]):
            result = speed * (times[i] - speed)
            if result > distances[i]:
                wins += 1
        results.append(wins)
    return math.prod(results)

print('Part 1:', solve())

times     = [int(lines[0].split(':')[1].replace(' ',''))]
distances = [int(lines[1].split(':')[1].replace(' ',''))]

print('Part 2:', solve())
