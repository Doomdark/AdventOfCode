numbers = []
sums = {}
plen = 25

with open("Day09_input.txt") as f:
    for line in f.readlines():
        num = int(line.rstrip())
        numbers.append(num)

def part1():
    # How many iterations?
    for i in range(plen,len(numbers)-plen):
        sums = {}
        # Work out the sums for the previous plen numbers
        for s in range(i-plen,i):
            for x in range(s,i):
                sums[numbers[x]+numbers[s]] = 1
        # Is the current number in that list?
        if numbers[i] not in sums:
            print ("Part1:", numbers[i])
            return numbers[i]

invalid_number = part1()

def part2():
    # How many iterations?
    for i in range(len(numbers)-1):
        for j in range(i+1,len(numbers)):
            #print (i,j)
            if sum(numbers[i:j]) == invalid_number:
                #print (min(numbers[i:j]))
                print ("Part2:", min(numbers[i:j]) + max(numbers[i:j]))
                return

part2()
