boxes = []

with open("day02_input.txt") as f:
    for line in f.readlines():
        l,w,h = [int(x) for x in line.strip().split('x')]
        boxes.append((l,w,h))

def get_area(l,w,h):
    sides = [2*l*w, 2*w*h, 2*l*h]
    return sum(sides) + min(sides)/2

def get_ribbon(l,w,h):
    perimeters = [2*l+2*w, 2*w+2*h, 2*l+2*h]
    smallest = min(perimeters)
    volume = l*w*h
    return smallest + volume

total = 0
for box in boxes:
    l,w,h = box
    total += get_area(l,w,h)

print("Part 1:", total)

total = 0
for box in boxes:
    l,w,h = box
    total += get_ribbon(l,w,h)

print("Part 2:", total)
