lines = [ 'ADVENT',
          'A(1x5)BC',
          '(3x3)XYZ',
          'A(2x2)BCD(2x2)EFG',
          '(6x1)(1x3)A',
          'X(8x2)(3x3)ABCY' ]

line = ''

with open("day09_input.txt") as f:
    line = f.read().strip().replace(' ','')

def decompress(s):
    posn = 0
    out = ''
    numchars = 0
    multiples = 0
    in_marker = False
    in_chars = False
    multiple_string = None

    for char in s:
        #print(char)
        # Not processing a marker
        if not in_marker:
            if numchars > 0:
                multiple_string += char
                numchars -= 1
                if numchars == 0:
                    for i in range(multiples):
                        out += multiple_string
            elif char == '(':
                multiples = ''
                numchars = ''
                in_marker = True
                in_chars = True
            else:
                out += char

        else: # In marker
            if char == ')':
                multiples = int(multiples)
                numchars = int(numchars)
                in_marker = False
                in_multiples = False
                multiple_string = ''
            elif char == 'x':
                in_multiples = True
                in_chars = False
            elif in_chars:
                numchars += char
            elif in_multiples:
                multiples += char

    return out

#for line in lines:
print("Part 1:", len(decompress(line)))

# Part 2 - keep decompressing until the length stops changing
first = True
done = False
length = 0
final = ''

while not done:
    newline = decompress(line)

    # Check if there are any more markers
    if '(' not in newline:
        final = newline
        length = len(newline)
        done = True

    print(len(newline))

    line = newline

print("Part 2:", length)
