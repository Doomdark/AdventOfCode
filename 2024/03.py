memory = open('03.in').read()

import re

mul_match = re.compile(r'mul\((\d+),(\d+)\)')

matches = mul_match.findall(memory)

total = sum([int(a)*int(b) for a,b in matches])

print('Part 1:', total)

matcher = re.compile(r"(do)\(\)|(don't)\(\)|(mul)\((\d+),(\d+)\)")

matches = matcher.findall(memory)

total = 0
enabled = True

for match in matches:
    if match[1] == "don't": enabled = False
    elif match[0] == "do": enabled = True
    elif enabled:
        total += int(match[3])* int(match[4])

print('Part 2:', total)
