from itertools import combinations

weapons = [( 8, 4, 0),
           (10, 5, 0),
           (25, 6, 0),
           (40, 7, 0),
           (74, 8, 0)]

armour = [(  0, 0, 0),
          ( 13, 0, 1),
          ( 31, 0, 2),
          ( 53, 0, 3),
          ( 75, 0, 4),
          (102, 0, 5)]

rings = [(  0, 0, 0),
         ( 25, 1, 0),
         ( 50, 2, 0),
         (100, 3, 0),
         ( 20, 0, 1),
         ( 40, 0, 2),
         ( 80, 0, 3)]

# For each possible combination, apply the fighting rules

class Char:
    def __init__(self, hp, damage, armour):
        self.hp = hp
        self.damage = damage
        self.armour = armour

    def attack(self, other):
        doing_damage = self.damage - other.armour
        if doing_damage < 1:
            doing_damage = 1
        other.hp -= doing_damage

least_gold = 100000
most_gold = 0

# Try each possibility
for w in weapons:
    for a in armour:
        for rl, rr in combinations(rings, 2):
            
            me_cost   = w[0] + a[0] + rl[0] + rr[0]
            me_damage = w[1] + a[1] + rl[1] + rr[1]
            me_armour = w[2] + a[2] + rl[2] + rr[2]

            me   = Char(100, me_damage, me_armour)
            boss = Char(103, 9, 2)

            while True:
                me.attack(boss)
                # I win! Update the least gold count
                if boss.hp <= 0:
                    least_gold = min(least_gold, me_cost)
                    break
                boss.attack(me)
                if me.hp <= 0:
                    most_gold = max(most_gold, me_cost)
                    break
        
print("Part 1:", least_gold)
print("Part 2:", most_gold)
