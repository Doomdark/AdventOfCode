def update_pos( c, p ):
    return { '>': (p[0] + 1, p[1]), '<': (p[0] - 1, p[1]), '^': (p[0], p[1] + 1), 'v': (p[0], p[1] - 1), '':(p[0],p[1]) }[c];

with open('day03_input.txt', 'rt') as f:
    content = f.read()
    pos = [(0, 0), (0,0)]
    visited_houses = { (0,0): True }
    for i in range( len(content)):
        print(i,content[i])
        t = pos[i%2] = update_pos(content[i].strip(), pos[i%2])
        visited_houses[t] = True
    print(len(visited_houses))
