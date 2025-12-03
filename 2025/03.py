# Read the input
lines = open("03.in").read().splitlines()

import itertools, operator

joltage = []

for line in lines:
    largest = 0
    numbers = [int(x) for x in line]
    for i in range(len(numbers)):
        for j in range(i+1,len(numbers)):
            combo = int(f"{numbers[i]}{numbers[j]}")
            if combo > largest:
                largest = combo
    joltage.append(largest)

print("Part 1:", sum(joltage))

joltage = 0

for line in lines:
    numbers = [int(x) for x in line]
    num = 0

    # Find the 12 largest numbers in order
    for i in range(11, -1, -1):
        # Make a list of the numbers upto the ith location
        temp = numbers[: len(numbers) - i]
        # Max value in the temp list
        _max = max(temp)
        # Index of the max value
        index = temp.index(_max)
        # Start at the new array index and look for the next highest number
        numbers = numbers[index + 1 :]
        # Add on the new value
        num = num * 10 + _max

    joltage += num

print("Part 2:", joltage)
