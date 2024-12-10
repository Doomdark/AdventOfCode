G = open('10.in').read().splitlines()

max_r = len(G)
max_c = len(G[0])

moves = [(-1,0), (1,0), (0,-1), (0,1)]

def dfs(visited, ends, trails, G, r, c, path):
    nvisited = visited | set((r,c))
    npath = path + [(r,c)]
    if G[r][c] == '9':
        ends.add((r,c))
        trails.add(tuple(npath))
        return
    for dr,dc in moves:
        nr,nc = r+dr,c+dc
        if nr>=0 and nr<max_r and nc>=0 and nc <max_c:
            if (nr,nc) not in nvisited and int(G[r][c]) + 1 == int(G[nr][nc]):
                dfs(nvisited, ends, trails, G, nr, nc, npath)

part1 = 0
trails = set()

for r in range(max_r):
    for c in range(max_c):
        if G[r][c] == '0':
            ends = set()
            dfs(set(), ends, trails, G, r, c, [])
            part1 += len(ends)

print('Part 1:', part1)
print('Part 2:', len(trails))
