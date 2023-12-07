moves = open("9.in").read().splitlines()

def manhattan_distance(a,b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def chebyshev_distance(a,b):
    return max(abs(a[1]-b[1]),abs(a[0]-b[0]))

def move_head(h, d):
    x,y = h
    if   d == 'U': y += 1
    elif d == 'D': y -= 1
    elif d == 'R': x += 1
    elif d == 'L': x -= 1
    return (x,y)

def move_knot(t, h):
    # If the abs difference of h and t is 1 for x and y then don't move the tail
    tx,ty = t
    hx,hy = h
    # Check for u/d and l/r first
    if ty == hy:
        if   tx > hx and tx - hx == 2: tx -= 1
        elif tx < hx and hx - tx == 2: tx += 1
    elif tx == hx:
        if   ty > hy and ty - hy == 2: ty -= 1
        elif ty < hy and hy - ty == 2: ty += 1
    # Move the tail if the head is more than 2 away from the tail
    #elif manhattan_distance(t,h) > 2:
    elif chebyshev_distance(t,h) > 1:
        # Move in a diagonal in the direction of the head
        if hx > tx:
            tx += 1
            if   hy > ty: ty += 1
            elif hy < ty: ty -= 1
        elif hx < tx:
            tx -= 1
            if   hy > ty: ty += 1
            elif hy < ty: ty -= 1
    return (tx,ty)

def do_moves():
    for move in moves:
        m = move.strip().split()
        direction = m[0]
        distance = int(m[1])
        for i in range(distance):
            for knot in range(len(knots)):
                if knot == 0:
                    knots[knot] = move_head(knots[knot], direction)
                else:
                    # Now move the knots depending on where the head is relative to the knot
                    knots[knot] = move_knot(knots[knot], knots[knot-1])
                    # Add the tail on
                    if knot == len(knots)-1:
                        tail_visited.add(knots[knot])

## Part 1 ##

knots = [(0,0)] * 2
tail_visited = set()
do_moves()
print('Part 1:',len(tail_visited))

## Part 2 ##

knots = [(0,0)] * 10
tail_visited = set()
do_moves()
print('Part 2:',len(tail_visited))
