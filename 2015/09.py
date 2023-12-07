from collections import defaultdict, deque
import re

lines = open("09.in").read().splitlines()

cities = defaultdict(dict)

p = re.compile('(\w+) to (\w+) = (\d+)')

for line in lines:
    src, dst, dist = p.match(line).groups()
    cities[src][dst] = int(dist)
    cities[dst][src] = int(dist)

shortest = 100000
longest  = 0

for src in cities:
    q = deque()
    start = (src, {src}, 0)
    q.append(start)
    while q:
        current, visited, dist = q.popleft()
        # Are we done with this state?
        if len(visited) == len(cities):
            shortest = min(shortest, dist)
            longest  = max(longest, dist)
            continue

        # Go to other places
        for city in cities:
            if city not in visited:
                new_dist = dist + cities[current][city]
                new_visited = {city} | visited
                q.append((city, new_visited, new_dist))

print('Part 1:', shortest)
print('Part 2:', longest)
