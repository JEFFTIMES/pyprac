import pprint as pp

# the base case: 
# when it reaches the last coords (8,8), if a number is given, returns True.
# if an empty spot is given, tries to find a number from 1 to 9 which fulfills the rules of sudoku,
# updates the spot on the board with the chosen number and returns True when the rules are fulfilled,
# otherwise returns False without updates the board.

# the other cases:
# if the given spot has a number, recursively calls the procedure for the next spot, otherwise
# tries a number from 1 to 9 to fill up the spot, updates the spot on the board and recursively call
# itself to process the spot on the next coords if achieved, or returns False if failed.
# waits for the following recursive procedure's return, return True when receives a True, otherwise, 
# does the clean job on the maps before return False.


# helper function: initializes the maps with the given numbers on the board. 
def initialize_maps(board, maps):  
  for row in range(9):
    for col in range(9):
      b_row, b_col = row // 3, col // 3
      e = board[row][col]
      if e != '.':
        number = int(e)
        if number <1 or number >9:
          raise ValueError('Invalid number.')
        maps['row'][row][number] = 1
        maps['col'][col][number] = 1
        maps['block'][b_row][b_col][number] = 1
  return True

# helper function: validates the number for the given spot against the maps of the row, the col and the block.
def is_satisfied(number, coords, maps):
  row, col = coords
  b_row, b_col = row // 3, col // 3
  satisfied = True
  #checks all the three maps, if any of them violates the rules, set the satisfied to False
  if maps['row'][row][number] == 1 or maps['col'][col][number] == 1 or maps['block'][b_row][b_col][number] == 1:
    satisfied = False
  # update the corresponding spots of all the three maps to record the visiting if satisfied.
  if satisfied:
    maps['row'][row][number] = 1 
    maps['col'][col][number] = 1
    maps['block'][b_row][b_col][number] = 1 
  return satisfied

# helper function: restores the values of the maps correspond to the given spot.
def restore_maps(number, coords, maps):
  row, col = coords
  b_row, b_col = row // 3, col // 3
  maps['row'][row][number] = 0
  maps['col'][col][number] = 0
  maps['block'][b_row][b_col][number] = 0
  return True

# helper function: helps the recursive call to iterate through the board.
def get_next_coords(coords):
  row, col = coords
  if row < 0 or row > 8:
    raise ValueError(f'invalid row index {row}')
  if col < 0  or col >8:
    raise ValueError(f'invalid col index {col}')
  if col == 8:
    row +=1
    col = 0
  else: 
    col +=1
  return row, col


def sudoku_solvers(coords, board, maps=None, counts=[0]):
  if maps == None:
    r_map = [[0]*10 for i in range(9)]
    c_map = [[0]*10 for i in range(9)]
    b_map = [[[0]*10 for i in range(3)] for j in range(3)]
    maps = {
      'row': r_map, 
      'col': c_map, 
      'block': b_map,
      }
    initialize_maps(board, maps) 
  
  # count the numbers of the recursive calls
  counts[0] += 1

  # the base condition
  if coords == (8,8):
    row, col = coords
    e = board[row][col] 
    if e != '.':    # a given number
      return True
    else:           # an empty spot
      for n in range(1,10):
        if is_satisfied(n, coords, maps):
          board[row][col] = str(n)
          return True
      return False
  
  # the other cases
  row, col = coords
  next_coords = get_next_coords(coords)
  e = board[row][col]
  if e != '.':    # a given number
    return sudoku_solvers(next_coords, board, maps, counts)
  else:           # an empty spot, try 1 to 9 to find a solution
    for n in range(1,10):
      if is_satisfied(n, coords, maps):  
        board[row][col] = str(n)
        if not sudoku_solvers(next_coords, board, maps, counts):  # False returned from the following call, do the clean up
          board[row][col] = '.'
          restore_maps(n, coords, maps)
        else:
          return True
    return False


if __name__ == '__main__':
  board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
counts=[0]
pp.pprint(board)
pp.pprint(sudoku_solvers((0,0),board, counts=counts))
pp.pprint(board)
pp.pprint(counts)
