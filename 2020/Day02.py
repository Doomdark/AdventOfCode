import re
passwords = []
valid = 0

parse = re.compile('(\d+)-(\d+) (\w): (\w+)')

with open("Day02_input.txt") as f:
    for line in f.readlines():
        match = parse.match(line.strip())
        if match:
            min = int(match.group(1))
            max = int(match.group(2))
            letter = match.group(3)
            pwd = match.group(4)
            passwords.append((min, max, letter, pwd))

def part1():
    valid = 0
    for min, max, letter, pwd in passwords:
        num = sum([x == letter for x in pwd])
        if num >= min and num <= max:
            valid += 1
    print "Part1:", valid

part1()

def part2():
    valid = 0
    for pos1, pos2, letter, pwd in passwords:
        a = pwd[pos1-1] == letter
        b = pwd[pos2-1] == letter
        if a != b:
            valid += 1
    print "Part2:", valid

part2()
