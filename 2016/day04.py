import collections
import re

rooms = []

with open("day04_input.txt") as f:
    for line in f.readlines():
        rooms.append(line.strip())

id_sum = 0

def valid_check(room):
    values = {}
    l = re.match(r'([a-z\-]+)(\d+)\[([a-z]+)\]', room)
    # Get the parts of the room
    name = l.groups()[0].replace('-','')
    sector_id = int(l.groups()[1])
    checksum = l.groups()[2]

    # Get the most common letters in the name
    most_common = collections.Counter(name).most_common(26)

    # Make a dictionary of values:count to group the letters with the same counts
    for letter, count in most_common:
        if count not in values:
            values[count] = []
        values[count].append(letter)

    # Now construct the checksum of the decreasing values:
    calc_checksum = ''
    for count, letters in values.items():
        calc_checksum += ''.join(sorted(letters))

    # Only compare the first 5 letters in the calculated checksum
    if checksum == calc_checksum[0:5]:
        return sector_id
    else:
        return 0

# Store the valid rooms
valid_rooms = []

for room in rooms:
    valid = valid_check(room)
    id_sum += valid
    if valid:
        valid_rooms.append(room)

print("Part 1:", id_sum)

def decrypt(room):
    l = re.match(r'([a-z\-]+)(\d+)', room)
    # Get the useful parts of the room
    name = l.groups()[0].replace('-',' ')
    sector_id = int(l.groups()[1])

    # Advance all the letters in the room name sector_id times
    for i in range(sector_id):
        new_name = ''
        # Check each character in the name
        for char in name:
            # Space doesn't change
            if char == ' ':
                new_name += char
            # z goes back to a
            elif char == 'z':
                new_name += 'a'
            else:
                # Increment to the next letter along
                new_name += chr(ord(char)+1)

        # Update for the next iteration
        name = new_name
    return name, sector_id

for room in sorted(valid_rooms):
    decrypted, sector_id = decrypt(room)
    # Where's the north pole stuff?
    if 'north' in decrypted:
        print("Part 2:", decrypted, sector_id)
        break
