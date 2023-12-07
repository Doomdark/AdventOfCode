from collections import deque

def solve(qlen=256, part2=False):
    # Keep track of how much we've rotated the list so we can rotate it back later
    total_rot = 0
    skip_size = 0
    q = deque()
    
    if part2:
        nums = [ord(x) for x in open('10.in').read().rstrip()]
        nums.extend([17, 31, 73, 47, 23])
    else:
        nums = [int(x) for x in open('10.in').read().rstrip().split(',')]

    for i in range(qlen):
        q.append(i)
        
    count = 64 if part2 else 1
    
    for _ in range(count):
        for num in nums:
            ql = deque()
            for i in range(num):
                ql.append(q.popleft())
            #print('0',ql,q)
            qp = deque(reversed(ql))
            for i in range(num):
                q.insert(0,qp.pop())
            #print('1',q)
            rot = num+skip_size
            q.rotate(-rot)
            skip_size += 1
            total_rot += rot
            #print(q)

    # Return the list back to its proper place
    q.rotate(total_rot)

    if part2:
        xors = []
        for i in range(16):
            _xor = 0
            for j in range(16):
                _xor ^= q[(i*16)+j]
            xors.append(_xor)
        
        return ''.join(['{:02x}'.format(a) for a in xors])
    else:
        return q[0]*q[1]
    
print('Part 1:', solve())
print('Part 2:', solve(part2=True))
