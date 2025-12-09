# Read the input
lines = open("09.in").read().splitlines()

tiles = []
edges = set()
filled = set()

minx, maxx, miny, maxy = 10**12,0,10**12,0

def make_edge(a,b):
    lx,ly = b
    x,y = a
    if x == lx:
        for ny in range(min(y,ly), max(y,ly)+1):
            edges.add((x,ny))
    if y == ly:
        for nx in range(min(x,lx), max(x,lx)+1):
            edges.add((nx,y))

for line in lines:
    x,y = map(int, line.split(','))
    minx = min(minx,x)
    maxx = max(maxx,x)
    miny = min(miny,y)
    maxy = max(maxy,y)
    if len(tiles) > 0:
        make_edge((x,y), tiles[-1])
    tiles.append((x,y))
# Link the last and first tiles
make_edge(tiles[0], tiles[-1])

biggest = 0

for tile1 in tiles:
    x1,y1 = tile1
    for tile2 in tiles:
        x2,y2 = tile2
        if tile2 == tile1: continue
        x = max(x1,x2) - min(x1,x2) + 1
        y = max(y1,y2) - min(y1,y2) + 1
        area = x * y
        biggest = max(area, biggest)

print('Part 1:', biggest)

def print_grid():
    for y in range(miny,maxy+1):
        line = ''
        for x in range(minx,maxx+1):
            if (x,y) in filled:
                line += '#'
            else:
                line += '.'
        print(line)

filled.update(set(tiles))
filled.update(edges)

def fill(point):
    Q = [point]
    filled.add(point)
    while Q:
        (x,y) = Q.pop()
        filled.add((x,y))
        for dy,dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx,ny = x+dx,y+dy
            if (nx,ny) not in filled:
                filled.add((nx,ny))
                Q.append((nx,ny))

startx = min([x for x,y in edges])
starty = min([y for x,y in tiles if x == startx])
fill((startx+1, starty+1))

#print_grid()
#exit(1)

biggest = 0

for tile1 in tiles:
    x1,y1 = tile1
    for tile2 in tiles:
        x2,y2 = tile2
        if tile2 == tile1: continue

        # Test if the rectangle perimeter covered by these corners is in the filled set
        covered = True
        min_x, max_x = min(x1,x2), max(x1,x2)
        min_y, max_y = min(y1,y2), max(y1,y2)

        for ny in [min_y,max_y]:
            for nx in range(min_x, max_x+1):
                if (nx,ny) not in filled:
                    covered = False
                    break
            if not covered:
                break

        if not covered:
            continue

        for nx in [min_x,max_x]:
            for ny in range(min_y, max_y+1):
                if (nx,ny) not in filled:
                    covered = False
                    break
            if not covered:
                break

        if covered:
            x = max_x - min_x + 1
            y = max_y - min_y + 1
            area = x * y
            biggest = max(area, biggest)

print('Part 2:', biggest)
