loc = (0,0)

locs = set()
locs.add(loc)

moves = open("day03_input.txt").read()

#moves = "^v^v^v^v^v"
#moves = '^>v<'
#moves = '^v'

def move_santa(loc, m):
    x,y = loc
    if   m == '^': y += 1
    elif m == 'v': y -= 1
    elif m == '>': x += 1
    elif m == '<': x -= 1
    nloc = (x,y)
    return nloc

for move in moves:
    nloc = move_santa(loc, move)
    locs.add(nloc)
    loc = nloc

print("Part 1:", len(locs))

santa_loc = (0,0)
robo_loc  = (0,0)

locs = set()
locs.add(loc)

for count, move in enumerate(moves):
    if count %2 == 0:
        nloc_santa = move_santa(santa_loc, move)
        locs.add(nloc_santa)
        santa_loc = nloc_santa
    else:
        nloc_robo = move_santa(robo_loc, move)
        locs.add(nloc_robo)
        robo_loc = nloc_robo

print("Part 2:", len(locs))
