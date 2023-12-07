sizes = []
positions = []

with open("day15_input.txt") as f:
    for line in f.readlines():
        l = line.strip().split()
        sizes.append(int(l[3]))
        positions.append(int(l[11].split('.')[0]))

#sizes = [17,3,19,13,7,5,11]
#positions = [15,2,4,2,2,0,0]

# Where do we have to end up if this is going to work?
targetPositions = [-i%sizes[i] for i in range(len(sizes))]

time = 0
while True:
    if [(positions[i]+time) % sizes[i] for i in range(len(positions))] == targetPositions:
        print("Part 1:", time-1)
        break
    time += 1

sizes.append(11)
positions.append(0)

targetPositions = [-i%sizes[i] for i in range(len(sizes))]

time = 0
while True:
    if [(positions[i]+time) % sizes[i] for i in range(len(positions))] == targetPositions:
        print("Part 2:", time-1)
        break
    time += 1
