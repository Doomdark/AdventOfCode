sensors_dict = {}
sensors = set()
beacons = set()

lines = open("15.in").read().splitlines()
#lines = open("15ex.in").read().splitlines()

def manhattan_distance(a,b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])

for line in lines:
    ss,bb = line.split(': ')
    sss = ss.split(', ')
    sx = int(sss[0].split('=')[1])
    sy = int(sss[1].split('=')[1])
    bbb = bb.split(', ')
    bx = int(bbb[0].split('=')[1])
    by = int(bbb[1].split('=')[1])
    sensors_dict[(sx,sy)] = (bx,by,manhattan_distance((sx,sy),(bx,by)))
    sensors.add((sx,sy,manhattan_distance((sx,sy),(bx,by))))
    beacons.add((bx,by))

def part1(y = 2000000):
    # Store where the coverage is
    coverage = set()

    # Iterate over the sensors to make a coverage map for just the specified row
    for sc,sensor in enumerate(sensors):
        sx,sy,dist = sensor
        bx,by,dist = sensors_dict[(sx,sy)]
        max_x = sx+dist
        min_x = sx-dist
        max_y = sy+dist
        min_y = sy-dist
        # Set the coverage if the sensor can see this point
        for x in range(min_x,max_x+1):
            # Point is already in the coverage
            if (x,y) in coverage:
                continue
            _dist = manhattan_distance((sx,sy),(x,y))
            # If the distance is within the sensor->beacon distance then it's covered
            if _dist <= dist and (x,y) not in beacons:
                coverage.add((x,y))

    coverage_row = [x for x,y in coverage]
    print('Part 1:',len(coverage_row))

part1()

## Part 2 ##

def valid(x,y,s):
    for (sx,sy,d) in s:
        dist = manhattan_distance((x,y),(sx,sy))
        # If the distance is less than the Mahattan distance away then it's invalid
        if dist <= d:
            return False
    return True

def part2():
    # If there is only one possible position for another beacon then it must be distance d+1 from some sensor.
    for (sx,sy,d) in sensors:
        # Check all points that are d+1 away from (sx,sy)
        for dx in range(d+2):
            dy = (d+1)-dx
            # Try all 4 corners of the coordinate d+1 away from the sensor.
            # This multiplies the dx/dy by 1/-1 to get the up/down/left/right slopes of the coverage diamond
            for signx,signy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                x = sx+(dx*signx)
                y = sy+(dy*signy)
                # It's not inside the specified boundaries
                if not(0<=x<=4000000 and 0<=y<=4000000):
                    continue
                # If the position is not inside any sensor range then it's the point we're looking for
                if valid(x,y,sensors):
                    #print(n_checked,x,y)
                    print('Part 2:',x*4000000 + y)
                    return

part2()
