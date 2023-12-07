numbers = []

with open("Day01_input.txt") as f:
    for line in f.readlines():
        numbers.append(int(line.strip()))

# Loop through all then numbers
def get_2020(nums):
    for i, num in enumerate(nums):
        for j in range(i, len(nums)):
            if num + nums[j] == 2020:
                return num * nums[j]

#print "Part 1:", get_2020(numbers)

# Loop through all then numbers
def get_2020_2(nums):
    for i, num in enumerate(nums):
        for j in range(i, len(nums)):
            for k in range(j, len(nums)):
                if num + nums[j] + nums[k] == 2020:
                    return num * nums[j] * nums[k]

print "Part 2:", get_2020_2(numbers)

