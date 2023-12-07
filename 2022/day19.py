import re
import multiprocessing as mp

lines = open("19.in").read().splitlines()

blueprints = []

for line in lines:
    numbers = re.findall('\d+', line)
    blueprints.append([int(x) for x in numbers])

# Process a blueprint using BFS
def do_blueprint(b, T):
    # Read the input
    num, ore_cost_ore, clay_cost_ore, ob_cost_ore, ob_cost_clay, geode_cost_ore, geode_cost_ob = b

    # What's the maximum resource required to build any robot?
    max_required_ore  = max([ore_cost_ore, clay_cost_ore, ob_cost_ore, geode_cost_ore])
    max_required_clay = ob_cost_clay
    max_required_ob   = geode_cost_ob

    # Somewhere to store the current state
    q = set()

    # State - q.add((ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, T))
    q.add((1, 0, 0, 0, 0, 0, 0, 0))

    # Each update takes 1 minute
    for time in range(T-1,-1,-1):

        # New set for destination states
        newq = set()

        # Iterate through each state in the current time step
        for item in q:

            # Current state
            ore_bots, clay_bots, ob_bots, geode_bots, _ore, _clay, _obsidian, _geodes = item

            # Make new resources with existing robots
            new_ore    = _ore + ore_bots
            new_clay   = _clay + clay_bots
            new_ob     = _obsidian + ob_bots
            new_geodes = _geodes + geode_bots

            # Can we not build some bots?
            build_ore_bots  = True
            build_clay_bots = True
            build_ob_bots   = True

            # If we have as many bots as required to make enough resources to build any non-geode
            # robot every minute then don't build any more robots.
            if ore_bots  >= max_required_ore:  build_ore_bots  = False
            if clay_bots >= max_required_clay: build_clay_bots = False
            if ob_bots   >= max_required_ob:   build_ob_bots   = False

            # If: bots * remaining time + current stock >= maximum required resource * remaining time
            # then we don't need to make any more bots for that resource.
            if ore_bots  * time + _ore      >= time * max_required_ore : build_ore_bots  = False
            if clay_bots * time + _clay     >= time * max_required_clay: build_clay_bots = False
            if ob_bots   * time + _obsidian >= time * max_required_ob  : build_ob_bots   = False

            # Make a geode robot
            if _ore >= geode_cost_ore and _obsidian >= geode_cost_ob:
                new = (ore_bots, clay_bots, ob_bots, geode_bots+1,
                       new_ore-geode_cost_ore, new_clay, new_ob-geode_cost_ob, new_geodes)
                if new not in newq:
                    newq.add(new)
            # Make an obsidian robot
            if _ore >= ob_cost_ore and _clay >= ob_cost_clay and build_ob_bots:
                new = (ore_bots, clay_bots, ob_bots+1, geode_bots,
                       new_ore-ob_cost_ore, new_clay-ob_cost_clay, new_ob, new_geodes)
                if new not in newq:
                    newq.add(new)
            # Make a clay robot
            if _ore >= clay_cost_ore and build_clay_bots:
                new = (ore_bots, clay_bots+1, ob_bots, geode_bots,
                       new_ore-clay_cost_ore, new_clay, new_ob, new_geodes)
                if new not in newq:
                    newq.add(new)
            # Make an ore robot
            if _ore >= ore_cost_ore and build_ore_bots:
                new = (ore_bots+1, clay_bots, ob_bots, geode_bots,
                       new_ore-ore_cost_ore, new_clay, new_ob, new_geodes)
                if new not in newq:
                    newq.add(new)
            # Also maintain the current state as that's a possible outcome too
            new = (ore_bots, clay_bots, ob_bots, geode_bots,
                   new_ore, new_clay, new_ob, new_geodes)
            if new not in newq:
                newq.add(new)
        # Save the new queue for the next time iteration
        q = newq
        #print(num, time, len(q))

    max_geodes = max([geodes for a,b,c,d,e,f,g,geodes in q])
    print(num, '...', max_geodes)
    return max_geodes


def solve(T, blueprints, part2=False):
    
    quality = 1 if part2 else 0
    
    for num,b in enumerate(blueprints):
        gc = do_blueprint(b, T)
        
        if part2:
            quality *= gc
        else:
            quality += gc*(num+1)
 
    return quality

print("Part 1:",solve(24, blueprints))

## Part 2 ##

blue2 = blueprints[:3]
print("Part 2:",solve(32, blue2, True))
