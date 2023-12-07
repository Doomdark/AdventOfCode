triangles  = []
impossible = []

with open("day03_input.txt") as f:
    for line in f.readlines():
        tri = [int(x) for x in line.split()]
        triangles.append(tri)

def get_impossibles(tris):
    impossibles = []
    for triangle in tris:
        x,y,z = triangle
        if (x+y)<=z:
            impossibles.append(triangle)
            continue
        if (z+y)<=x:
            impossibles.append(triangle)
            continue
        if (z+x)<=y:
            impossibles.append(triangle)
            continue
    return impossibles

impossibles = get_impossibles(triangles)

print("Part 1:", len(triangles) - len(impossibles))

transposed = []

def transpose(tris):
    grouped = []
    count = 0
    for tri in tris:
        grouped.append(tri)
        count += 1

        # Done 3
        if count == 3:
            for i in range(3):
                newtri = [t[i] for t in grouped]
                transposed.append(newtri)
            grouped = []
            count = 0

transpose(triangles)

impossibles = get_impossibles(transposed)

print("Part 2:", len(triangles) - len(impossibles))
