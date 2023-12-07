coord = [0,0]
facing = 'E'
dirs = {'N' :{'y':-1,'x':+0},
        'NE':{'y':-1,'x':+1},
        'E' :{'y':+0,'x':+1},
        'SE':{'y':+1,'x':+1},
        'S' :{'y':+1,'x':+0},
        'SW':{'y':+1,'x':-1},
        'W' :{'y':+0,'x':-1},
        'NW':{'y':-1,'x':-1} }

import re
filt = re.compile('(\w)(\d+)')

def move(coord, dir, number):
    if dir == 'N':
        coord[0] += number
    elif dir == 'E':
        coord[1] += number
    elif dir == 'S':
        coord[0] -= number
    elif dir == 'W':
        coord[1] -= number
    return coord

def rotate(facing, dir, angle):
    if dir == 'R':
        if angle == 90:
            if   facing == 'N': facing = 'E'
            elif facing == 'E': facing = 'S'   
            elif facing == 'S': facing = 'W'   
            elif facing == 'W': facing = 'N'
        elif angle == 180:
            if   facing == 'N': facing = 'S'
            elif facing == 'E': facing = 'W'   
            elif facing == 'S': facing = 'N'   
            elif facing == 'W': facing = 'E'
        elif angle == 270:
            if   facing == 'N': facing = 'W'
            elif facing == 'E': facing = 'N'   
            elif facing == 'S': facing = 'E'   
            elif facing == 'W': facing = 'S'
    else:
        if angle == 90:
            if   facing == 'N': facing = 'W'
            elif facing == 'E': facing = 'N'   
            elif facing == 'S': facing = 'E'   
            elif facing == 'W': facing = 'S'
        elif angle == 180:
            if   facing == 'N': facing = 'S'
            elif facing == 'E': facing = 'W'   
            elif facing == 'S': facing = 'N'   
            elif facing == 'W': facing = 'E'
        elif angle == 270:
            if   facing == 'N': facing = 'E'
            elif facing == 'E': facing = 'S'   
            elif facing == 'S': facing = 'W'   
            elif facing == 'W': facing = 'N'
    return facing

def distance(coord):
    return abs(coord[0]) + abs(coord[1])

with open("Day12_input.txt") as f:
    for line in f.readlines():
        match = filt.match(line.rstrip())
        dir = match.group(1)
        number = int(match.group(2))

        if dir in ['N','E','S','W']:
            coord = move(coord, dir, number)
        elif dir == 'F':
            coord = move(coord, facing, number)
        elif dir in ['R','L']:
            facing = rotate(facing, dir, number)

    print ("Part 1:", distance(coord))

# Part 2

# Waypoint offset to the ship
way = [1,10]
coord = [0,0]

def move_to_way(coord, way, number):
    for i in range(number):
        coord[0] += way[0]
        coord[1] += way[1]
    return coord

def rotate_way(way, dir, angle):
    _way = [0,0]
    if angle == 180:
        _way[0] = -way[0]
        _way[1] = -way[1]
    elif angle == 90:
        if dir == 'R':
            _way[0] = -way[1]
            _way[1] =  way[0]
        else:
            _way[0] =  way[1]
            _way[1] = -way[0]
    elif angle == 270:
        if dir == 'L':
            _way[0] = -way[1]
            _way[1] =  way[0]
        else:
            _way[0] =  way[1]
            _way[1] = -way[0]
    return _way

with open("Day12_input.txt") as f:
    for line in f.readlines():
        match = filt.match(line.rstrip())
        dir = match.group(1)
        number = int(match.group(2))

        if dir in ['N','E','S','W']:
            way = move(way, dir, number)
        elif dir == 'F':
            coord = move_to_way(coord, way, number)
        elif dir in ['R','L']:
            way = rotate_way(way, dir, number)

    print ("Part 2:", distance(coord))

