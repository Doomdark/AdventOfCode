#instructions = [
#    'rect 3x2',
#    'rotate column x=1 by 1',
#    'rotate row y=0 by 4',
#    'rotate column x=1 by 1'
#    ]

instructions = []

with open("day08_input.txt") as f:
   for line in f.readlines():
       instructions.append(line.strip())

grid = set()

max_x = 50
max_y = 6

def draw_grid(g):
    for y in range(max_y):
        line = ''
        for x in range(max_x):
            if (x,y) in grid:
                line += '#'
            else:
                line += '.'
        print(line)

for inst in instructions:
    inst_list = inst.split()

    # Turn on pixels
    if inst_list[0] == 'rect':
        x,y = [int(x) for x in inst_list[1].split('x')]
        for i in range(x):
            for j in range(y):
                # This pixel is now on
                grid.add((i,j))

    # Rotate pixels
    elif inst_list[0] == 'rotate':
        newgrid = set()
        # North to south rotation
        if inst_list[1] == 'column':
            col   = int(inst_list[2].split('=')[1])
            value = int(inst_list[4])
            # Keep the old grid for other columns
            for pixel in grid:
                x,y = pixel
                if x != col:
                    newgrid.add(pixel)
                else:
                    ny = (y + value) % max_y
                    newgrid.add((x,ny))

        elif inst_list[1] == 'row':
            row   = int(inst_list[2].split('=')[1])
            value = int(inst_list[4])
            # Keep the old grid for other columns
            for pixel in grid:
                x,y = pixel
                if y != row:
                    newgrid.add(pixel)
                else:
                    nx = (x + value) % max_x
                    newgrid.add((nx,y))

        grid = newgrid

print("Part 1:", len(grid))

print("Part 2:")
draw_grid(grid)
