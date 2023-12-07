from collections import defaultdict

lines = open('15.in').read().splitlines()

ingredients = defaultdict(dict)

for line in lines:
    l = line.split(': ')
    ingredient = l[0]
    ll = l[1].split(', ')
    for lll in ll:
        name, value = lll.split()
        ingredients[ingredient][name] = int(value)

# Try all the ingredients
highest = 0
highest_part2 = 0
a_name = 'Sprinkles'
b_name = 'PeanutButter'
c_name = 'Frosting'
d_name = 'Sugar'
for a in range(0,101):
    a_capacity   = ingredients[a_name]['capacity']   * a
    a_durability = ingredients[a_name]['durability'] * a
    a_flavour    = ingredients[a_name]['flavor']     * a
    a_texture    = ingredients[a_name]['texture']    * a
    a_calorie    = ingredients[a_name]['calories']   * a
    for b in range(0,101):
        b_capacity   = ingredients[b_name]['capacity']   * b
        b_durability = ingredients[b_name]['durability'] * b
        b_flavour    = ingredients[b_name]['flavor']     * b
        b_texture    = ingredients[b_name]['texture']    * b
        b_calorie    = ingredients[b_name]['calories']   * b
        for c in range(0,101):
            c_capacity   = ingredients[c_name]['capacity']   * c
            c_durability = ingredients[c_name]['durability'] * c
            c_flavour    = ingredients[c_name]['flavor']     * c
            c_texture    = ingredients[c_name]['texture']    * c
            c_calorie    = ingredients[c_name]['calories']   * c
            for d in range(0,101):
                if a+b+c+d != 100:
                    continue
                d_capacity   = ingredients[d_name]['capacity']   * d
                d_durability = ingredients[d_name]['durability'] * d
                d_flavour    = ingredients[d_name]['flavor']     * d
                d_texture    = ingredients[d_name]['texture']    * d
                d_calorie    = ingredients[d_name]['calories']   * d

                capacity   = max(0, sum([a_capacity,   b_capacity,   c_capacity,   d_capacity  ]))
                durability = max(0, sum([a_durability, b_durability, c_durability, d_durability]))
                flavour    = max(0, sum([a_flavour,    b_flavour,    c_flavour,    d_flavour   ]))
                texture    = max(0, sum([a_texture,    b_texture,    c_texture,    d_texture   ]))
                calorie    = max(0, sum([a_calorie,    b_calorie,    c_calorie,    d_calorie   ]))

                total = capacity * durability * flavour * texture
                highest = max(total, highest)
                if calorie == 500:
                    highest_part2 = max(total, highest_part2)

print('Part 1:',highest)
print('Part 2:',highest_part2)
