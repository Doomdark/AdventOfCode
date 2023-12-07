turns = []

with open("day02_input.txt") as f:
    for line in f.readlines():
        turns.append(line.strip())

rock     = ['A','X']
paper    = ['B','Y']
scissors = ['C','Z']

def get_part1_score(y,m):
    if m in rock:
        if y in scissors: return 6 + 1 # win
        if y in rock:     return 3 + 1 # draw
        if y in paper:    return 0 + 1 # lose
    elif m in paper:
        if y in scissors: return 0 + 2 # lose
        if y in rock:     return 6 + 2 # win
        if y in paper:    return 3 + 2 # draw
    elif m in scissors:
        if y in scissors: return 3 + 3 # draw
        if y in rock:     return 0 + 3 # lose
        if y in paper:    return 6 + 3 # win

total = 0

for turn in turns:
    you, me = turn.split()
    total += get_part1_score(you, me)

print("Part 1:", total)

def get_part2_score(y, result):
    if result in 'X': # lose
        if y in scissors: return 0 + 2 # paper
        if y in rock:     return 0 + 3 # scissors
        if y in paper:    return 0 + 1 # rock
    elif result in 'Y': # draw
        if y in scissors: return 3 + 3 # scissors
        if y in rock:     return 3 + 1 # rock
        if y in paper:    return 3 + 2 # paper
    elif result in 'Z': # win
        if y in scissors: return 6 + 1 # rock
        if y in rock:     return 6 + 2 # paper
        if y in paper:    return 6 + 3 # scissors

total = 0

for turn in turns:
    you, result = turn.split()
    total += get_part2_score(you, result)

print("Part 2:", total)
