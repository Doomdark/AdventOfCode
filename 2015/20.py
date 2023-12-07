import math
from collections import defaultdict

def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor

target = 34000000

# Get all the divisors for the house number

def part1():
    for house in range(target):
       
       # Get all the elves (divisors)
       divisors = list(divisorGenerator(house))
       
       # Each elf devlivers 10 presents
       total = int(10*sum(divisors))

       # Reached the target yet?
       if total >= target:
          print('Part 1:', house)
          return

def part2():
    # Store how many elves have delivered presents
    delivered = defaultdict(int)
    
    for house in range(target):
       # Get all the divisors
       divisors = list(divisorGenerator(house))
    
       # Remove any divisors that have been used 50 times already
       divisors2 = [x for x in divisors if delivered.get(x, 0) < 50]
       
       # Each elf delivers 11 presents
       total = int(11*sum(divisors2))
    
       # Update the elf delivery counts
       for d in divisors2:
          delivered[d] += 1

       # Reached the target yet?
       if total >= target:
          print('Part 2:', house)
          return

part1()
part2()


