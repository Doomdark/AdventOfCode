q = []
c = 0
part1 = []
part2 = []
p1 = None
p2 = None

line = open("day06_input.txt").read()
for char in line:
    c += 1
    # Add the char to the list
    q.append(char)
    # Got p1 yet?
    if p1 is None:
        # Last 4 chars for part 1
        if len(q) > 4:
            part1 = q[-4:]
        # If they're all different then that's part 1
        if len(set(part1)) == 4:
            p1 = c
    # Got p2 yet?
    if p2 is None:
        # Last 14 chars for part 2
        if len(q) > 14:
            part2 = q[-14:]
        # If they're all different then that's the end
        if len(set(part2)) == 14:
            p2 = c
            break

print("Part 1:", p1)
print("Part 2:", p2)
