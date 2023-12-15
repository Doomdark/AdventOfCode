line = open('15.in').read().splitlines()

def get_hash(string):
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current %= 256
    return current

def part1():
    total = 0
    for code in line[0].split(','):
        val = get_hash(code)
        total += val
    print('Part 1:', total)

part1()

# Part 2

# Make a 256-entry list of dictionaries
boxes = [{} for _ in range(256)]

def part2():
    # Process the instructions
    for code in line[0].split(','):
        box = 0
        marker = ''
        focal_length = 0

        # Remove
        if '-' in code:
            marker = code.split('-')[0]
            box = get_hash(marker)
            boxes[box].pop(marker, -1)
        # Add/replace
        else:
            marker, focal_length = code.split('=')
            box = get_hash(marker)
            # Dictionary items are ordered by earliest first
            boxes[box][marker] = int(focal_length)

    total = 0

    # Sum up all the lists
    for box_index, box in enumerate(boxes):
        for lens_index, (marker, focal_length) in enumerate(box.items()):
            total += (box_index + 1) * (lens_index + 1) * focal_length

    print("Part 2:", total)

part2()
