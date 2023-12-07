import copy

def apply_curve(a):
    b = a[::-1]
    nb = ''.join([('0' if x == '1' else '1') for x in b])
    return a + '0' + nb

def checksum(data):
    c = data
    nc = ''
    while True:
        for i in range(0, len(c), 2):
            if c[i] == c[i+1]:
                nc += '1'
            else:
                nc += '0'

        if len(nc) %2 == 1:
            return nc
        else:
            c = nc
            nc = ''

def fill_disk(size, data):
    while len(data) < size:
        data = apply_curve(data)
    # Return the first size characters
    return data[:size]

data = fill_disk(272, '01000100010010111')
print('Part 1:',checksum(data))

data = fill_disk(35651584, '01000100010010111')
print('Part 2:',checksum(data))
