with open("Day25_input.txt") as f:
    lines = f.read().splitlines()
    keys = [int(line) for line in lines]

def transform(num=1, subject_number=7):
    return (num * subject_number) % 20201227

def find_loop_count(public_key, subject_number=7):
    value = 1
    loops = 1
    while True:
        value = transform(value)
        if value == public_key:
            break
        loops += 1
    return loops

def get_encryption_key(subject_number, loops):
    value = 1
    for i in range(loops):
        value = transform(value, subject_number)
    return value

#loops = [find_loop_count(x) for x in keys]

#print("Part 1:", get_encryption_key(keys[0], loops[1]))

print(pow(keys[0], find_loop_count(keys[1]), 20201227))
