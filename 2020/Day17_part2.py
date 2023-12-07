cycles = 7

start_grid = []

with open("Day17_input.txt") as f:
    for line in f.readlines():
        row = []
        for char in line.rstrip():
            row.append(char)
        start_grid.append(row)

# How big will the grid become after <cycles> have elapsed?
grid_max_x = (cycles*2) * len(start_grid[0])
grid_max_y = (cycles*2) * len(start_grid)
grid_max_z =  cycles*2 + 1
grid_max_w =  cycles*2 + 1
grid_start_x_min = cycles
grid_start_x_max = cycles + len(start_grid[0])
grid_start_y_min = cycles
grid_start_y_max = cycles + len(start_grid)
grid_start_z_min = cycles
grid_start_z_max = cycles + 1
grid_start_w_min = cycles
grid_start_w_max = cycles + 1

def print_grid_2d(grid,cycle):    
    cycle_range_max_x = cycles + cycle + len(start_grid[0])
    cycle_range_min_x = cycles - cycle
    cycle_range_max_y = cycles + cycle + len(start_grid)
    cycle_range_min_y = cycles - cycle
    for c,row in enumerate(grid):
        if c in range(cycle_range_min_y, cycle_range_max_y):
            print(''.join(row[cycle_range_min_x:cycle_range_max_x]))
    print()

def print_grid_3d(grid,cycle):
    cycle_range_max = cycles + cycle + 1
    cycle_range_min = cycles - cycle
    for c,z in enumerate(grid):
        if c in range(cycle_range_min, cycle_range_max):
            print("z =",c-cycles)
            print_grid_2d(z,cycle)
    print()

# Make a grid of that size
def new_grid():
    g = []
    for w in range(grid_max_w):
        _z = []
        for z in range(grid_max_z):
            _y = []
            for y in range(grid_max_y):
                _x = []
                for x in range(grid_max_x):
                    _x.append('.')
                _y.append(_x)
            _z.append(_y)
        g.append(_z)
    return g

grid = new_grid()

# Place the start grid into the 3D grid
for cy,y in enumerate(start_grid):
    for cx,x in enumerate(y):
        grid[cycles][cycles][cy+cycles][cx+cycles] = start_grid[cy][cx]

#print_grid_3d(grid,0)

def check_coord(grid,x,y,z,w):
    neighbours = []
    for _w in range(w-1,w+2):
        for _z in range(z-1,z+2):
            for _y in range(y-1,y+2):
                for _x in range(x-1,x+2):
                    if not ((_z==z) and (_y==y) and (_x==x) and (_w==w)):
                        neighbours.append(grid[_w][_z][_y][_x])
    active_count = sum([x=='#' for x in neighbours])
    if grid[w][z][y][x] == '#':
        if active_count in [2,3]:
            return '#'
    elif grid[w][z][y][x] == '.':
        if active_count == 3:
            return '#'
    return '.'

# OK, now do the actual game of life thing
for n in range(cycles-1):
    iteration = n+1
    print("Cycle", iteration)
    _grid = new_grid()
    for _w in range(grid_start_w_min-iteration, grid_start_w_max+iteration):
        for _z in range(grid_start_z_min-iteration, grid_start_z_max+iteration):
            for _y in range(grid_start_y_min-iteration, grid_start_y_max+iteration):
                for _x in range(grid_start_x_min-iteration, grid_start_x_max+iteration):
                    _grid[_w][_z][_y][_x] = check_coord(grid,_x,_y,_z,_w)
        print("-",_w)
    grid = _grid
    #print_grid_3d(grid,iteration)

# Part 2 - sum the active nodes
def part2(grid):
    total = 0
    for w in grid:
        for z in w:
            for y in z:
                for x in y:
                    total += (x == '#')

    return total

print("Part 2:", part2(grid))

