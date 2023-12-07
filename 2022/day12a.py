from collections import deque

grid = [list(x) for x in open("12.in").read().strip().splitlines()]

sr = 0
sc = 0
er = 0
ec = 0

# Construct the map
for r,row in enumerate(grid):
    for c,char in enumerate(row):
        if char == 'S':
            sr = r
            sc = c
            grid[r][c] = 'a'
        elif char == 'E':
            er = r
            ec = c
            grid[r][c] = 'z'

q = deque()
q.append((0,sr,sc))

seen = {(sr,sc)}

while q:
    d,r,c = q.popleft()
    for nr,nc in [(r+1,c), (r-1,c), (r,c+1), (r,c-1)]:
        # Off grid
        if nr<0 or nr>=len(grid) or nc<0 or nc>=len(grid[0]):
            continue
        # Already seen
        if (nr,nc) in seen:
            continue
        # Can't get to that square
        if ord(grid[nr][nc]) - ord(grid[r][c]) > 1:
            continue
        # End?
        if nr == er and nc == ec:
            print("Part 1:",d+1)
            exit(0)
        # Add new location
        seen.add((nr,nc))
        # Go to the new place?
        q.append((d+1,nr,nc))
