import collections

lines = []

with open("day06_input.txt") as f:
   for line in f.readlines():
       lines.append(line.strip())

# Now which character is the most common for each row.
part1_message = ''
part2_message = ''

for i in range(len(lines[0])):
    column = ''.join([x[i] for x in lines])
    most_common = collections.Counter(column).most_common(26)[0][0]
    part1_message += most_common
    least_common = collections.Counter(column).most_common(26)[-1][0]
    part2_message += least_common

print("Part 1:", part1_message)
print("Part 2:", part2_message)
