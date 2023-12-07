grid    = []
visible = []

lines = open("8.in").read().splitlines()

def print_grid(grid, ones=False):
    for row in range(len(grid)):
        r = ''
        for col in range(len(grid[0])):
            if ones:
                r += '0' if grid[row][col] else '.'
            else:
                r += '{}'.format(grid[row][col])
        print(r)

def sum_grid(grid):
    count = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            count += 1 if grid[row][col] else 0
    return count

# Parse the input
for line in lines:
    l = line.strip()
    row = [int(x) for x in l]
    vrow = [False for x in l]
    grid.append(row)
    visible.append(vrow)

#print_grid(grid)

## Part 1 ##

# Mark all the edges as visible
for col in range(len(grid[0])):
    visible[0][col] = True
    visible[-1][col] = True
for row in range(len(grid)):
    visible[row][0] = True
    visible[row][-1] = True

# Go across the top side and see if the trees are visible from there
for col in range(len(grid[0])):
    tallest = 0
    for row in range(len(grid)):
        if grid[row][col] > tallest:
            visible[row][col] = True
            tallest = grid[row][col]

# Now across the bottom
for col in range(len(grid[0])):
    tallest = 0
    for row in range(len(grid)-1,0,-1):
        if grid[row][col] > tallest:
            visible[row][col] = True
            tallest = grid[row][col]

# Now down the left
for row in range(len(grid)):
    tallest = 0
    for col in range(len(grid[0])):
        if grid[row][col] > tallest:
            visible[row][col] = True
            tallest = grid[row][col]

# Now down the right
for row in range(len(grid)):
    tallest = 0
    for col in range(len(grid[0])-1,0,-1):
        if grid[row][col] > tallest:
            visible[row][col] = True
            tallest = grid[row][col]

print("Part 1:", sum_grid(visible))
#print_grid(visible, True)

## Part 2 ##

def get_scenic_score(row,col,h):
    l,r,u,d = 1,1,1,1

    # Left
    if col == 0:
        l = 0
    else:
        for _c in range(col-1,0,-1):
            # If we've stopped at the edge break out of the loop
            if _c == 0:
                break
            if grid[row][_c] < h:
                l += 1
            else:
                break

    # Right
    if col == len(grid[0])-1:
        r = 0
    else:
        for _c in range(col+1,len(grid[0])):
            # If we've stopped at the edge break out of the loop
            if _c == len(grid[0]) - 1:
                break
            if grid[row][_c] < h:
                r += 1
            else:
                break

    # Down
    if row == len(grid)-1:
        d = 0
    else:
        for _r in range(row+1,len(grid)):
            # If we've stopped at the edge break out of the loop
            if _r == len(grid) - 1:
                break
            if grid[_r][col] < h:
                d += 1
            else:
                break

    # Up
    if row == 0:
        u = 0
    else:
        for _r in range(row-1,0,-1):
            # If we've stopped at the edge break out of the loop
            if _r == 0:
                break
            if grid[_r][col] < h:
                u += 1
            else:
                break

    #print(row,col, h, l*r*u*d, l,r,u,d)
    return l*r*u*d

#print(get_scenic_score(3,4,grid[3][4]))
#print(get_scenic_score(3,2,grid[3][2]))

score = 0
for row in range(len(grid)):
    for col in range(len(grid[0])):
        sscore = get_scenic_score(row,col,grid[row][col])
        if sscore > score:
            score = sscore

print("Part 2:",score)
