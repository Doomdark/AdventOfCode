# Read the input
lines = open("12.in").read().splitlines()

Pieces = {}
Regions = []
index = None

for line in lines:
    if 'x' in line:
        r,q = line.split(': ')
        x,y = [int(a) for a in r.split('x')]
        Regions.append( ((x,y), [int(x) for x in q.split()]) )
    # New piece
    elif ':' in line:
        index = int(line[:-1])
        piece = 0
    elif '#' in line:
        for char in line:
            if char == '#':
                piece += 1
    else:
        Pieces[index] = piece

fits = 0

# Just see if the number of #'s in each shape fits in the area of the region
for (x,y), counts in Regions:
    area = x*y
    total = sum([Pieces[i]*x for i,x in enumerate(counts)])
    if total <= area:
        fits += 1

print('Part 1:', fits)
