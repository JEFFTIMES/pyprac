import random


# given a new column and the positions[], checks if placing the queen at the new place conflict with
# the exists queens.
# the r of the new place comes from the len(positions), the c is given by the input
# conflict occurs when c == positions[i] or abs(c-position[i]) == r-i : for i in range(len(positions)) 
def conflict(c, positions):
    # get number of the row to be tested
    r = len(positions)
    
    for i in range(len(positions)):
        if c == positions[i] or abs(c-positions[i]) == r-i: # abs(c-position[i]) in (0, r-i)
            return True
    return False


def queens(n, positions=()):
    
    if len(positions) == n-1:   # reach the last row
        for c in range(n):      # check each of the column 
            if not conflict(c, positions):   # find a position
                print('base yield: ', c)
                yield (c,)      # yield a position              
    else:                       # the other lines
        for c in range(n):      # check each of the column
            if not conflict(c, positions):   # when positions = (0,2)
                for result in queens(n, positions + (c,)):
                    print('recur yield: ', (c,) + result)
                    yield (c,) + result
            

def queens2(n, positions=()):
  
    for c in range(n):      # check each of the column of the given row.
        
        print('check conflict: row:', len(positions), '\tcolumn:', c ,'\t input positions: ', positions)
        conf = conflict(c, positions)
        print('conflict with exists?\t', conf)
        
        # if the checking position c conflict with the existing positions, do nothing with it and
        # goes on to the next position until exhausts any column.
        
        if not conf:     
            
            """
            if the checked position (row=len(positions), col=c) does not conflict with 
            the existing positions and the given row is not the last row, recursively 
            call the function with the checked position c added to the positions which 
            passed to the function to find out the rest qualified positions, then yield 
            this position plus the positions yield from the recursive calls.
            otherwise, it reaches the base condition, the last row, yield the checked position.
            """
            if len(positions) != n-1:    # not the last row
                print('recursively call itself  to check row:', len(positions+(c,)), '\tcolumn:', c, '\t input positions:', positions + (c,))
                for result in queens2(n, positions + (c,)):
                    print('recur yield: ', (c,) + result)
                    yield (c,) + result
            else:                        #len(positions) == n-1, the last row
                print('base yield: ', c)
                yield (c,)

def pretty_print(solution):
    def line(position, length=len(solution)):
        return '.' * position + 'X' + '.' * (length-position-1)
    for pos in solution:
        print(line(pos))



def test():
  res = list(queens2(8))
  pretty_print(random.choice(res))    

if __name__ == '__main__':
  test()