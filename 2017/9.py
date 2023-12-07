in_garbage = False
score = 0
level = 1
ignore = False

lines = open("9.in").read().splitlines()

chars = 0

for line in lines:
   # print(line)
    for char in line:
        #print(char)
        if ignore:
            ignore = False
        elif char == '!':
            ignore = True
        elif in_garbage:
            if char == '>':
                in_garbage = False
            else:
                chars += 1
        elif char == '<':
            in_garbage = True
        elif char == '{':
            score += level
            level += 1
        elif char == '}':
            level -= 1

print('Part 1:', score)
print('Part 2:', chars)
