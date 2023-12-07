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
#key = 'wenycdww'

grid = []

count = 0

ones = set()

for i in range(128):
    _input = '{}-{}'.format(key,i)
    #print(_input)
    _hash = knot_hash(_input)
    #print(_hash)
    hash_num = int(_hash,16)
    hash_bin = '{:b}'.format(hash_num)
    count += hash_bin.count('1')
    for x in range(len(hash_bin)):
      if hash_bin[x] == '1':
        ones.add((x,i))

print(count)

# Part 2

from collections import defaultdict

regions = defaultdict(list)

def get_adjacents(loc):
    x,y = loc
    adjs = set()
    for dx,dy in [(0,-1), (0,1), (-1,0), (1,0)]:
        nx,ny = x+dx,y+dy
        if ((nx,ny)) in ones:
           adjs.add((nx,ny))
    return adjs

region_num = 0
done = set()

from collections import deque

for (x,y) in ones:

    done_adjs = set()
  
    if (x,y) in done:
      continue
    
    # For each 1, check for adjacent 1s
    q = deque()
    q.append((x,y,region_num))

    while q:
        cx,cy,rn = q.pop()
        regions[rn].append((cx,cy))
        
        # Get the adjacent ones
        adjs = get_adjacents((cx,cy))
        for ax,ay in adjs:
            if (ax,ay) not in done_adjs:
                q.append((ax,ay,rn))
                done_adjs.add((ax,ay))
                
        done.add((cx,cy))
                
    region_num += 1
  

print(len(regions))


