from collections import defaultdict
import re, copy

lines = open('09.in').read().splitlines()
sequences = defaultdict(list)

# Read all the sequences in
for line in lines:
    nums = [int(x) for x in re.findall('[-\d]+', line)]
    sequences[tuple(nums)] = []

# Add the new diffs lists into each existing list of diffs
for seq,diffslist in sequences.items():
    diffs = seq
    # Check if all diffs are 0
    while not all([x==0 for x in diffs]):
        ndiffs = []
        # Find the diffs for all the numbers in the list
        for i in range(len(diffs)-1):
            diff = diffs[i+1] - diffs[i]
            ndiffs.append(diff)
        # Append the new diffs list to the list of lists
        diffslist.append(ndiffs)
        diffs = ndiffs

def solve(part2=False):
    vals = []
    # Append for part 1, prepend for part 2
    index = 0 if part2 else -1

    # Iterate through the sequences and diffs
    for seq,diffslist in sequences.items():
        adder = 0
        # Append/prepend the current adder to all the next list
        for i in range(len(diffslist)-1,-1,-1):
            val = diffslist[i][index]
            new_val = val - adder if part2 else val + adder
            # Prepend the adder for part 2, append it for part 1
            if part2: diffslist[i].insert(0, new_val )
            else:     diffslist[i].append(   new_val )
            # Update the adder for the next diff list
            adder = diffslist[i][index]
        # Calculate the value to add to the original sequence
        val = seq[index]-adder if part2 else seq[index]+adder
        # Add the final value to the list to sum at the end
        vals.append(val)
    # Return the answer
    return sum(vals)

print('Part 1:', solve())
print('Part 2:', solve(True))
