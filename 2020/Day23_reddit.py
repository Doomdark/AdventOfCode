class Cup():
    def __init__(self, id):
        self.id = id
        self.next = None

numstring = '716892543'

def part_2():
    cups = {}

    nums = [int(num) for num in numstring]

    # Initial cups
    for num in nums:
        cups[num] = Cup(num)

    # Additional cups
    for num in range(10, 1000001):
        cups[num] = Cup(num)

    # Connect the first cups to their next in line...
    for i in range(len(nums) - 1):
        cups[nums[i]].next = cups[nums[i + 1]]

    # ...and all the other cups to the next in sequence
    cups[nums[len(nums) - 1]].next = cups[10]
    for i in range(10, 1000000):
        cups[i].next = cups[i + 1]
    # Connect the last cup back to the 0th cup
    cups[1000000].next = cups[nums[0]]

    # Start at the first cup
    current_cup = cups[nums[0]]
    move = 0

    # Lots of moves
    while move < 10000000:
        # Get the next 3 cups
        removed_ids = [current_cup.next.id, current_cup.next.next.id, current_cup.next.next.next.id]
        # Set the current cup's next to skip over the 3 just removed
        current_cup.next = current_cup.next.next.next.next
        # The new destination cup is the current ID minus 1
        destination_cup_id = current_cup.id - 1
        # Unless it's 0, then wrap round
        if destination_cup_id == 0:
            destination_cup_id = 1000000
        # If the new id is in the list of removed ids then subtract 1
        while destination_cup_id in removed_ids:
            destination_cup_id -= 1
            # Wrap round if the new id is 0
            if destination_cup_id == 0:
                destination_cup_id = 1000000

        # The new destination cup is the cup at the final id from above
        destination_cup = cups[destination_cup_id]
        # Set the last-removed cup's next to be the new destination cup plus one
        cups[removed_ids[2]].next = destination_cup.next
        # Set the destination cup's next to be the first removed cup
        destination_cup.next = cups[removed_ids[0]]
        # Set the new cup to be the one to the right of the current cup
        current_cup = current_cup.next
        # Movin'
        move += 1

    # The two cups are the second and third in the list
    star_1 = cups[1].next.id
    star_2 = cups[1].next.next.id
    print (star_1, star_2)

    return star_1 * star_2

print("Part 2:",part_2())
