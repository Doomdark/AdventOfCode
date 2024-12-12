lines = open('12.in').read().splitlines()

from collections import defaultdict

max_r = len(lines)
max_c = len(lines[0])

def flood(r, c):
    global lines, SEEN
    Q = [(r,c)]
    PERIM = dict()
    perim = 0
    area = 0
    while Q:
        r,c = Q.pop()
        if (r,c) in SEEN:
            continue
        SEEN.add((r,c))
        area += 1
        for dr,dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr,nc = r+dr,c+dc
            # If we're on grid and the new square is in the same area then add it to the queue
            if 0<=nr<max_r and 0<=nc<max_c and lines[nr][nc] == lines[r][c]:
                Q.append((nr,nc))
            else: # New square is not in this area so this square is a perimeter to this area. Add it to the set based on the current direction.
                perim += 1
                if (dr,dc) not in PERIM:
                    PERIM[(dr, dc)] = set()
                PERIM[(dr,dc)].add((r,c))

    # Once we've got all the perimeter directions we can work out how many sides there are
    sides = 0
    for k,v in PERIM.items():
        PSEEN = set()
        # For each perimeter location in this direction
        for (pr,pc) in v:
            # Haven't seen this one before
            if (pr,pc) not in PSEEN:
                # New side
                sides += 1
                Q = [(pr,pc)]
                while Q:
                    r,c = Q.pop()
                    if (r,c) in PSEEN: continue
                    PSEEN.add((r,c))
                    # Try each direction
                    for dr,dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                        nr,nc = r+dr, c+dc
                        # If the new location is in the list then it's a continuation of this side
                        if (nr,nc) in v:
                            Q.append((nr,nc))

    return area, perim, sides

SEEN = set()
part1 = 0
part2 = 0
for r in range(max_r):
    for c in range(max_c):
        if (r,c) not in SEEN:
            area, perim, sides = flood(r, c)
            part1 += area*perim
            part2 += area*sides

print('Part 1:', part1)
print('Part 2:', part2)
