lines = open("25.in").read().splitlines()

def to_decimal(number):
    value = 0
    for posn,char in enumerate(number):
        multiplier = 5**(len(number)-posn-1)
        if   char == '2': value += 2*multiplier
        elif char == '1': value += multiplier
        elif char == '-': value -= multiplier
        elif char == '=': value -= 2*multiplier
    return value

def to_snafu(value):
    output = ''
    while value:
        # Remainder when dividing by 5
        rem = value % 5
        # Actually divide by 5
        value //= 5

        # Remainder is 2, 1, or 0
        if rem <= 2:
            # Add on the remainder directly
            output = str(rem) + output
        else: # Remainder is 3 or 4 so add on either -2 or -1. rem is only ever 3 or 4 here.
            output = "   =-"[rem] + output
            # Carry 1
            value += 1

    return output

d = sum([to_decimal(line) for line in lines])

print('Part 1:', to_snafu(d))
