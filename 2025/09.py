from collections import defaultdict
from itertools import combinations
from bisect import bisect

# Read the input
lines = open("09.in").read().splitlines()

tiles = []
edges = set()
perimeter = set()

# Make an edge between red tiles
def make_edge(a,b):
    lx,ly = b
    x,y = a
    if x == lx:
        for ny in range(min(y,ly), max(y,ly)+1):
            edges.add((x,ny))
    if y == ly:
        for nx in range(min(x,lx), max(x,lx)+1):
            edges.add((nx,y))

# Read in the input file
for line in lines:
    x,y = map(int, line.split(','))
    if len(tiles) > 0:
        make_edge((x,y), tiles[-1])
    tiles.append((x,y))
# Link the last and first tiles
make_edge(tiles[0], tiles[-1])

# Get the area of the provided tile pair
def get_area(a,b):
    x1,y1 = a
    x2,y2 = b
    x = max(x1,x2) - min(x1,x2) + 1
    y = max(y1,y2) - min(y1,y2) + 1
    return x * y

biggest = 0

# Do all times against each other to find the biggest
for tile1 in tiles:
    for tile2 in tiles:
        if tile2 == tile1: continue
        area = get_area(tile1,tile2)
        biggest = max(area, biggest)

print('Part 1:', biggest)

# Make a set with all the perimeter locations in it
perimeter.update(set(tiles))
perimeter.update(edges)

# Make a list of red tile pairs which decrease in area starting with the largest
decreasing_sizes = sorted( ((get_area(*pair), pair) for pair in combinations(tiles, r=2)), reverse=True )

y_lists = defaultdict(list)
x_lists = defaultdict(list)

# Make lists of the x vs y and y vs x coordinates
for x,y in perimeter:
    y_lists[x].append(y)
    x_lists[y].append(x)

# Sort the lists by value
for y_list in y_lists.values(): y_list.sort()
for x_list in x_lists.values(): x_list.sort()

# Determine if the provided red tile pair rectangle fits into the perimeter
def contains_rectangle(a,b):
    # Shrink the rectangle by 1 to avoid having to check for the edges intersecting
    x_min = min(a[0],b[0]) + 1
    x_max = max(a[0],b[0]) - 1
    y_min = min(a[1],b[1]) + 1
    y_max = max(a[1],b[1]) - 1
    # Test all four edges of the rectangle against all the perimeter locations
    if bisect(y_lists[x_min], y_min) != bisect(y_lists[x_min], y_max): return False
    if bisect(y_lists[x_max], y_min) != bisect(y_lists[x_max], y_max): return False
    if bisect(x_lists[y_min], x_min) != bisect(x_lists[y_min], x_max): return False
    if bisect(x_lists[y_max], x_min) != bisect(x_lists[y_max], x_max): return False
    # It fits!
    return True

# Test each tile pair against all the perimeter points from largest to smallest
for area, pair in decreasing_sizes:
    # The first one that fits is the largest
    if contains_rectangle(*pair):
        print('Part 2:', area)
        break
