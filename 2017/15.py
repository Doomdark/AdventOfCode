factors = [16807, 48271]
divider = 2147483647

def agen(part2=False):
    x = 591
    while True:
        x *= factors[0]
        x %= divider
        if part2:
            if x % 4 == 0:
                yield x
        else:
            yield x

def bgen(part2=False):
    x = 393
    while True:
        x *= factors[1]
        x %= divider
        if part2:
            if x % 8 == 0:
                yield x
        else:
            yield x

count = 0

A = agen()
B = bgen()

for _ in range(40000000):
    a = next(A)
    b = next(B)
    if a & 0xFFFF == b & 0xFFFF:
        count += 1

print('Part 1:', count)

count = 0

A = agen(True)
B = bgen(True)

for _ in range(5000000):
    a = next(A)
    b = next(B)
    if a & 0xFFFF == b & 0xFFFF:
        count += 1

print('Part 2:', count)
