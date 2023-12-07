def solve(row_count):
    row = '.^^.^^^..^.^..^.^^.^^^^.^^.^^...^..^...^^^..^^...^..^^^^^^..^.^^^..^.^^^^.^^^.^...^^^.^^.^^^.^.^^.^.'
    nrows = 1
    mi,ma = 0,len(row)-1
    safe_count = row.count('.')

    while nrows < row_count:
        nrow = ''
        for i in range(len(row)):
            crow = ''
            # Make the pattern matcher for this bit
            for j in [-1,0,1]:
                nj = i + j
                if mi<=nj<=ma:
                    crow += row[nj]
                else:
                    crow += '.'
    
            # Now pattern-match crow
            if crow in ['^^.', '.^^', '^..' , '..^']:
                nrow += '^'
            else:
                nrow += '.'

        safe_count += nrow.count('.')
        row = str(nrow)
        nrows += 1
    
    return safe_count

print('Part 1:', solve(40))
print('Part 2:', solve(400000))

    
