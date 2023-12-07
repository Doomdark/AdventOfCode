from hashlib import md5

key = "yzbqklnj"

index = 1
part1 = 0
part2 = 0
while True:
    string = key + str(index)
    md5hash = str(md5(string.encode('utf-8')).hexdigest())
    if md5hash.startswith('00000'):
        part1 = int(index)
    if md5hash.startswith('000000'):
        part2 = index
        break
    index += 1

print("Part 1:", part1)
print("Part 2:", part2)
