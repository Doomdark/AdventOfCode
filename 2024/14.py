lines = open('14.in').read().splitlines()

import math
from collections import deque

X = 101
Y = 103

class Robot:
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def move(self):
        nx = (self.p[0] + self.v[0]) % X
        ny = (self.p[1] + self.v[1]) % Y
        self.p = (nx, ny)

    def __str__(self):
        return '{} {} {}'.format(self.n, str(self.p), str(self.v))

def init():
    robots = []
    for line in lines:
        p,v = line.split()
        _p = p.split('=')
        px,py = [int(a) for a in _p[1].split(',')]
        _v = v.split('=')
        vx,vy = [int(a) for a in _v[1].split(',')]
        r = Robot((px,py), (vx,vy))
        robots.append(r)
    return robots

def quadrant_count(robots, tl, br):
    _robots = []
    tlx,tly = tl
    brx,bry = br
    for r in robots:
        rx,ry = r.p
        if tlx<=rx<=brx and tly<=ry<=bry:
            _robots.append(r)
    return len(_robots)

def part1(robots):
    counts = []
    hX = X//2
    hY = Y//2
    for i in range(100):
        for r in robots:
            r.move()
    # Get the quadrant counts, top left to bottom right
    for (tl,br) in [((0,0),(hX-1,hY-1)), ((hX+1,0),(X-1,hY-1)), ((0,hY+1),(hX-1,Y-1)), ((hX+1,hY+1),(X-1,Y-1))]:
        counts.append(quadrant_count(robots, tl,br))
    print('Part 1:', math.prod(counts))

part1(init())

# Part 2

def print_grid(robots):
    for y in range(Y):
        l = ''
        for x in range(X):
            R = False
            for r in robots:
                if r.p == (x,y):
                    l += '#'
                    R = True
                    break
            if not R:
                l += '.'
        print(l)

def flood(r, locations):
    Q = []
    SEEN = set()
    adj = 0
    Q.append(r.p)
    while Q:
        p = Q.pop()
        if p in SEEN: continue
        SEEN.add(p)
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            np = (p[0]+dx,p[1]+dy)
            if np in locations:
                adj += 1
                Q.append(np)
    return adj

def part2(robots):
    i = 0
    while True:
        i += 1
        adjacents = []
        locations = set()
        for r in robots:
            r.move()
            locations.add(r.p)
        for r in robots:
            # If a flood fill contains a 1/4 or more of the robots then that's the picture
            if flood(r, locations) >= len(robots)//4:
                print_grid(robots)
                print('Part 2:', i)
                return

part2(init())
