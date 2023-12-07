lines = open("08.in").read().splitlines()

def process(lines):
    extras = []

    for line in lines:
        _line = line[1:-1]
        i = 0
        backing = False
        while i < len(_line):
            if backing:
                if _line[i] == 'x': extra = 3
                else:               extra = 1
                extras.append(extra)
                i += extra
                backing = False
            elif _line[i] == '\\':
                backing = True
                i += 1
            else:
                i += 1

    return sum(extras) + len(lines)*2

part1 = process(lines)
print('Part 1:', part1)

# Add escape characters for quotes and backslashes
def escape(lines):
    lengths = []

    for line in lines:
        extra = 0
        for char in line:
            if char in ['"', '\\']:
                extra += 1
        lengths.append(extra+2)

    return sum(lengths)

part2 = escape(lines)
print('part 2:', part2)
