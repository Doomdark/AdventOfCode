from collections import deque

def knot_hash(data):
    data = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    l = [x for x in range(256)]
    i = 0
    skip_size = 0
    for _ in range(0,64):
        for d in data:
            for j in range(0,d // 2):
                l[(i + j) % len(l)], l[(i + (d - j - 1)) % len(l)] = l[(i + (d - j - 1)) % len(l)], l[(i + j) % len(l)]
            i += d + skip_size
            i = i % len(l)
            skip_size += 1
    
    dense_hash = []
    for i in range(16):
        x = 0
        for j in range(16):
            x = x ^ l[i*16 + j]
        dense_hash.append(x)
    
    s = ""
    for c in dense_hash:
        s += "{0:02x}".format(c)
    return s

key = 'flqrgnkx'
key = 'wenycdww'

count = 0
hashes = []

for i in range(128):
    _input = '{}-{}'.format(key,i)
    #print(_input)
    _hash = knot_hash(_input)
    #print(_hash)
    hash_num = int(_hash,16)
    hash_bin = '{:0>128b}'.format(hash_num)
    #print(hash_bin)
    count += hash_bin.count('1')
    # For part 2
    hashes.append(hash_bin)

print('Part 1:', count)

# Part 2

from collections import defaultdict

regions = defaultdict(int)

def get_adjacents(loc):
    x,y = loc
    adjs = []
    for dx,dy in [(0,-1), (0,1), (-1,0), (1,0)]:
        nx,ny = x+dx,y+dy
        if 0<=nx<128 and 0<=ny<128:
            if hashes[nx][ny] == '1':
                adjs.append((nx,ny))
    return adjs

region_count = 0
done = set()

from heapq import heappush, heappop

for x in range(128):
  for y in range(128):
    # Not a 1 so skip it
    if hashes[x][y] != '1': continue
    # Already seen this one in a previous fill
    if (x,y) in done: continue
    # Not see this before so it must be in a new region
    region_count += 1
    # For each 1, check for adjacent 1s
    q = []
    heappush(q, (x,y))
    # Run the BFS
    while q:
        cx,cy = heappop(q)
        # Already been here
        if (cx,cy) in done: continue
        done.add((cx,cy))
        # Get the adjacent ones
        for ax,ay in get_adjacents((cx,cy)):
            q.append((ax,ay))                
                
print('Part 2:', region_count)


