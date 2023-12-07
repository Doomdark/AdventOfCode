digits = '1113122113'

def process(instring, repeat=40):
    string = instring

    for i in range(repeat):
        current = (0,'0')
        outstring = ''
        val = None
        count = 0

        for digit in string:
            count, val = current

            if count == 0:
                current = (1, digit)
            else:
                if digit != val:
                    outstring += '{}{}'.format(count, val)
                    current = (1, digit)
                else:
                    current = (count+1, val)

        outstring += '{}{}'.format(current[0],current[1])
        string = outstring

    return outstring

print('Part 1:', len(process(digits)))
print('Part 2:', len(process(digits,50)))
