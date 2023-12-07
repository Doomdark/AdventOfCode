lights = {}

with open("day06_input.txt") as f:
    for line in f.readlines():
        if line.startswith('turn on'):
            l = line.strip().split()
            a,b,xy,thr,nxy = l
            x,y = [int(x) for x in xy.split(',')]
            nx,ny = [int(x) for x in nxy.split(',')]
            for _x in range(x,nx+1):
                for _y in range(y,ny+1):
                    if (_x,_y) not in lights:
                        lights[(_x,_y)] = 0
                    lights[(_x,_y)] += 1
        elif line.startswith('turn off'):
            l = line.strip().split()
            a,b,xy,thr,nxy = l
            x,y = [int(x) for x in xy.split(',')]
            nx,ny = [int(x) for x in nxy.split(',')]
            for _x in range(x,nx+1):
                for _y in range(y,ny+1):
                    if (_x,_y) in lights:
                        if lights[(_x,_y)] > 0:
                            lights[(_x,_y)] -= 1
        elif line.startswith('toggle'):
            l = line.strip().split()
            a,xy,thr,nxy = l
            x,y = [int(x) for x in xy.split(',')]
            nx,ny = [int(x) for x in nxy.split(',')]
            for _x in range(x,nx+1):
                for _y in range(y,ny+1):
                    if (_x,_y) not in lights:
                        lights[(_x,_y)] = 0
                    lights[(_x,_y)] += 2

print("Part 2:", sum([v for v in lights.values()]))
