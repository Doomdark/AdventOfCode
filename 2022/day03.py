# Store the sacks in a list
sacks = []

with open("day03_input.txt") as f:
    for line in f.readlines():
        l = line.strip()
        sack = {}
        # Split the line in half and make 2 compartments
        size = len(l)//2
        sack[1] = l[:size]
        sack[2] = l[size:]
        # Add on the compartmentalised sack to the list
        sacks.append(sack)

def get_priority(o):
    # ASCII range 97-122 is a-z
    char = ord(o)
    if char in range(97,123):
        return char - 97 + 1
    # Range 65-90 is A-Z
    elif char in range(65,91):
        return char - 65 + 27

part1 = 0

# Iterate through the sacks
for sack in sacks:
    # Use sets to find the common item
    common = list(set(sack[1]).intersection(set(sack[2])))
    part1 += get_priority(common[0])

print("Part 1:", part1)

part2 = 0

# Iterate through the sacks in threes
for i in range(0,len(sacks),3):
    # Append the first of the 3 sacks together
    sack0 = sacks[i][1] + sacks[i][2]
    sack1 = sacks[i+1][1] + sacks[i+1][2]
    sack2 = sacks[i+2][1] + sacks[i+2][2]
    # Use sets to find the common item
    common = list(set(sack0).intersection(set(sack1)).intersection(set(sack2)))
    part2 += get_priority(common[0])

print("Part 2:", part2)
