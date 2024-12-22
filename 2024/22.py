secrets = map(int, open('22.in').read().splitlines())

from collections import defaultdict, deque

def pseudo(secret):
    secret = (secret ^ (secret <<  6)) & 0xFFFFFF
    secret = (secret ^ (secret >>  5)) & 0xFFFFFF
    secret = (secret ^ (secret << 11)) & 0xFFFFFF
    return secret

part1 = 0

# Store the sales of bananas for each sequence for all secrets
totals = defaultdict(int)

# Process each secret
for secret in secrets:
    # Make a 4-long queue of changes
    changes = deque(maxlen=4)
    # Make a dictionary to store the first occurrence of each change sequence
    seen = set()
    # Run this 2000 times
    for n in range(2000):
        # Determine the first ones digit
        ones = secret % 10
        # New secret
        secret = pseudo(secret)
        # Next ones digit
        nones = secret % 10
        # Difference in the ones digit vs previous ones digit
        diff = nones - ones
        # Shove that diff into the changes list
        changes.append(diff)
        # If the deque has 4 entries
        if n>3:
            # Make a suitable sequence ID for the totals dictionary and seen set
            sequence = tuple(changes)
            # Capture only the first occurrence of this sequence
            if sequence not in seen:
                # Seen the first occurrence of this sequence for this secret
                seen.add(sequence)
                # Sum the values of all the first buys for this sequence for all secrets
                totals[sequence] += nones
    # Accumulate the total of the secret numbers
    part1 += secret

# Which sequence got the most bananas?
part2 = max(totals.values())

print('Part 1:', part1)
print('Part 2:', part2)
