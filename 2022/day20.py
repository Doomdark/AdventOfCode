from collections import deque
nums = deque()

# Read the input
lines = open("20.in").read().splitlines()

# Append the values to the list
for c,line in enumerate(lines):
    nums.append((c,int(line)))

# How long is the list?
moves = len(nums)

def permute(I):
    for i in range(I):
        for move in range(moves):
            # Get the item with the "move" value as the first element of the tuple
            entry = [x for x in nums if x[0] == move]
            # Find the index of the entry in the deque
            index = nums.index(entry[0])
            # Get the item value
            value = nums[index][1]
            # Skip the entry if the value is 0
            if value == 0: continue
            # Skip the entry if the value is the same as the length
            if abs(value) % abs(moves) == 0: continue
            # Rotate the deque to the index
            nums.rotate(-index)
            # Pop the item off the list
            item = nums.popleft()
            # Rotate the deque by the amount
            nums.rotate(-value)
            # Add the item in at the left
            nums.insert(0,item)

def get_sum(nums, indices):
    vals = []
    # Rotate the list until we reach the 0 value
    while (nums[0][1] != 0):
        nums.rotate(-1)
    # Find the values
    for i in range(max(indices)+1):
        if i in indices:
            vals.append(nums[0][1])
        nums.rotate(-1)
    return sum(vals)

permute(1)
print("Part 1:",get_sum(nums, [1000,2000,3000]))

## Part 2 ##

# Reinitialise nums with the encryption key
nums = deque()
for c,line in enumerate(lines):
    nums.append((c,int(line)*811589153))

permute(10)
print("Part 2:",get_sum(nums, [1000,2000,3000]))
