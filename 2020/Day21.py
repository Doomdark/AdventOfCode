foods = []
ingredients = {}

with open("Day21_input.txt") as f:
    lines = f.read().splitlines()
    for line in lines:
        bracket_split = line.split(' (contains ')
        # Put the ingredients in a set
        i = set(bracket_split[0].split())
        # Put the known allergens in a set too
        a = set()
        # There might not be any allergens listed
        if len(bracket_split) > 1:
            a = set(bracket_split[1][:-1].split(', '))
        # Now add the ingredients and allergens to the foods list
        foods.append((i,a))

#print("Foods:",foods)

# Make a list of all the ingredients and the number of times they appear in foods
foodCount = {}
# Make a list of allergens and the set of ingredients that they might be in
possible = {}

# Iterate through each food
for ingredients, allergens in foods:
    # For each ingredient, increment the foodCount for each time it appears in an ingredients list
    for ingredient in ingredients:
        if ingredient not in foodCount.keys():
            foodCount[ingredient] = 1
        else:
            foodCount[ingredient] += 1

    # For the allergens, add the possible ingredients to each allergen.
    for allergen in allergens:
        if allergen not in possible:
            possible[allergen] = ingredients.copy()
        else: # Update the allergen set to be the intersection of matching ingredients for this food
            possible[allergen] &= ingredients

# Which ingredients contribute to the list of allergens?
allergen_ingredients = set()
# Add every ingredient that is in the possible list as an allergen contributor.
for i in possible.values():
    allergen_ingredients.update(i)

# Subtract the ingredients that contribute to the allergens from the total list of
# ingredients to get those ingredients that don't contain allergens.
print("Part 1:", sum(foodCount[x] for x in (foodCount.keys() - allergen_ingredients)))

# Part 2 requires that all the allergens are identified to their ingredient.
# To do this:
# 1. Make a list containing all the fully-identified allergens so far. And a set with the identified ingredients.
# 2. For each allergen in the possible dictionary subtract the allergen's ingredients from the found ingredients set.
#    a. If the remaing set length = 1 then that's the ingredient for that allergen. Add to ingredients found set and allergen list.
#    b. If not then go on to the next allergen.
# 3. If the allergen list is shorter than the number of allergens in the possible dictionary then go round again.

#print([x for x in possible.keys()],'\n',[len(v) for v in possible.values()],'\n',[x for x in possible.values()])

ingredients_found = set()
allergens_dict = {}

# Keep going until all the allergens in the possible list have been matched
while len(allergens_dict.keys()) < len(possible.keys()):
    # Go through the items trying to find the matching allergens
    for allergen, ingredients in possible.items():
        # Subtract the found set from the current ingredients.
        # If there's only 1 left then that allergen matches that ingredient
        if len(ingredients - ingredients_found) == 1:
            # Fish the ingredient out of the remaining set
            ingredient = min(ingredients - ingredients_found)
            # Add it to the allergen map
            allergens_dict[allergen] = ingredient
            # Add the ingredient into the found set
            ingredients_found.add(ingredient)

# Print out the ingredients sorted alphabetically by allergen
print("Part 2:", ','.join([v for k,v in sorted(allergens_dict.items())]))

