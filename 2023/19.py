import re
from collections import defaultdict

# Read in the input file
f = open('19.in').read()
_flows, _parts = f.split('\n\n')
flows = _flows.strip().split('\n')
parts = _parts.strip().split('\n')

defaultrange = {'x':(1,4000), 'm':(1,4000), 'a':(1,4000), 's':(1,4000)}

# New function definition string
func_template = '''\
def {name}(part, ranges=defaultrange, part2=False):
   if part2:
      total = 0
      # Iterate through the workflow
      for i, (a, gtlt, threshold, dest1, dest2) in enumerate({order}):
          combs = 0
          passrange = None
          failrange = None
          # Copy the ranges for this iteration
          nranges = dict(ranges)
          # Set the destination workflow
          dest = dest2 if dest2 else dest1
          # Check if there's a new condition
          if a:
              # Current begin and end
              beg, end = ranges[a]
              # New threshold value
              val = int(threshold)
              # New range for this variable              
              if gtlt == '>':
                  passrange = (val+1, end)
                  failrange = (beg, val)
              else:
                  passrange = (beg, val-1)
                  failrange = (val, end)
              # Update the condition's pass range in the copy ofhe ranges
              nranges[a] = passrange
          # Get the values for the new condition if it's not rejected
          if dest != 'R':
              combs = eval("%s(None, nranges, part2)" % (dest.upper()))
              total += combs
          # Now update the dest range for the reverse range for the other items in this workflow
          if a:
              ranges[a] = failrange
      # Done
      return total
   else:
      {x}
'''

# Uppercase replacement in re.sub
def upper_repl(match):
    return match.group(1).upper()

accepted = defaultdict(int)

# Acceptance function
def A(part, ranges, part2):
    global accepted
    if part2:
        prod = 1
        # Multiply up all the ranges that reach this point
        for (beg,end) in ranges.values():
            prod *= (end-beg)+1
        return prod
    else:
        for k,v in part.items():
            accepted[k] += int(v)

# Rejection function
def R(part, ranges, part2):
    if part2:
        return 0
    
# Make a function for each workflow
for line in flows:
    name, flow = line.replace('{',' ').replace('}','').split(' ')
    # For part 2 add in a checking order for the xmas values
    _order = re.findall('(x|m|a|s)([<>])(\d+):([a-zA-Z]+)|,([a-zA-Z]+)(?=$)', flow)
    # Now replace all the workflow calls with function calls with the argument
    _flow = re.sub('(?<=[:])([a-zA-Z]+)(?=[,])', '\\1(part)', flow)
    # Match the last bit of the string
    _flow = re.sub('(?<=[,])([a-zA-Z]+)(?=$)', '\\1(part)', _flow)
    # Swap each a:b pair around
    _flow = re.sub(r'([0-9A-Za-z<>\(\)]+):([0-9A-Za-z<>\(\)]+)', '\\2:\\1', _flow)
    # Replace : with if and , with else
    _flow = _flow.replace(':',' if ').replace(',',' else ')
    # Now replace each of non-[x, m, a, s] string with am arg dictionary parts lookup
    _flow = re.sub('(([xmas])(?=[<>]))', "part['\\1']", _flow)
    # Uppercase the function names
    _flow = re.sub('([a-zA-Z]+)(?=\()', upper_repl, _flow)
    # Add the part2 string on
    _flow = re.sub('(\(part\))', '(part, ranges, part2)', _flow)
    # OK, we've got the execution string now so make the function. Uppercase the name because of "in"
    func = func_template.format(name=name.upper(), x=_flow, order=_order)
    # Create the workflow function with exec()
    exec(func)

# OK, now read in the parts
for p in parts:
    part = eval(re.sub('([xmas])(?==)', "'\\1'", p).replace('=',':'))
    IN(part)

print('Part 1:', sum([x for x in accepted.values()]))
print('Part 2:', IN(None, defaultrange, True))

    
