secrets = open('22.in').read().splitlines()

from collections import defaultdict, deque

def mix(val, secret):
    return val ^ secret

def prune(secret):
    return secret % (1<<24)

def pseudo(secret):
    mult1 = secret << 6 # *64
    mixed1 = mix(mult1, secret)
    secret1 = prune(mixed1)
    # ---
    divided2 = secret1 >> 5 # //32
    mixed2 = mix(secret1, divided2)
    secret2 = prune(mixed2)
    # ---
    mult3 = secret2 << 11 # *2048
    mixed3 = mix(secret2, mult3)
    secret3 = prune(mixed3)

    return secret3

def ones_digit(val):
    return int(val) % 10

part1 = 0

# Srote a list of first occurrences for each secret
first_list = []
# Store the total sales of bananas for each sequence for all secrets
totals = defaultdict(int)

# Process eachsecret
for secret in secrets:
    # Make a 4-long queue of changes
    changes = deque(maxlen=4)
    # Turn the secret into an integer
    secret = int(secret)
    # Determine the first ones digit
    ones = ones_digit(secret)
    # Make a dictionary to store the first occurrence of each change sequence
    first = defaultdict()
    # Run this 2000 times
    for n in range(2000):
        # New secret
        secret = pseudo(secret)
        # Next ones digit
        nones = ones_digit(secret)
        # Difference in the ones digit vs previous ones digit
        diff = nones - ones
        # Shove that into the changes list
        changes.append(diff)
        # If the deque has 4 entries
        if len(changes) == 4:
            # Make a suitable sequence ID for the dictionary
            sequence = tuple(changes)
            # Capture the first occurrence of this sequence
            if sequence not in first:
                first[sequence] = nones
                # Sum the values of all the first buys for this sequence for all secrets
                totals[sequence] += nones
        # Update the ones digit for the next iteration
        ones = nones
    # Add the first occurrence sequence dictionary to the list of firsts
    first_list.append(first)
    # Accumulate the total of the secret numbers
    part1 += secret

# Which sequence got the most bananas?
best = list(reversed([k for k, v in sorted(totals.items(), key=lambda item: item[1])]))[0]

part2 = 0
for first in first_list:
    # Sum the first sale of the best sequence for each secret
    if best in first:
        part2 += first[best]

print('Part 1:', part1)
print('Part 2:', part2)
