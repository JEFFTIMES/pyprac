'''
 
Input: [
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
Output: true

 
Input: [
  ["8","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: false

'''

# brute force solution, traverses all rows, all columns, 
# and all 3x3 blocks to check the duplicates of any 1-9 numbers.
def bf_validate_sudoku(board):
  # checks the rows
  for row in board:
    numbers = [0]*10
    for e in row:
      if e != '.':
        if int(e) <1 or int(e) > 9:
          raise ValueError("invalid number.")
        if numbers[int(e)] == 1:
          return False
        numbers[int(e)] += 1

  # checks the columns
  for col in range(9):
    numbers = [0]*10
    for coord_row in range(9):
      if board[coord_row][col] != '.':
        e = int(board[coord_row][col])
        if e <1 or e >9:
            raise ValueError('Invalid number.')
        if numbers[e] ==1:
          return False
        numbers[e] += 1
  
  # checks the 3x3 blocks
  for top_left_coords in [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]:
    numbers = [0]*10
    for row in range(top_left_coords[0], top_left_coords[0]+3):
      for col in range(top_left_coords[1],top_left_coords[1]+3):
        if board[row][col] != '.':
          e = int(board[row][col])
          if e <1 or e >9:
            raise ValueError('Invalid number.')
          if numbers[e] == 1:
            return False
          numbers[e] += 1
  
  return True



def validate_sudoku(board):
  
  def get_block_coords(coords):
    return coords[0]//3, coords[1]//3

  row_maps = [[0]*10 for i in range(9)]
  col_maps = [[0]*10 for i in range(9)]
  block_maps = [[[0]*10 for i in range(3)] for j in range(3)]

  for row in range(9):
    for col in range(9):
      if board[row][col] != '.':
        try:
          e = int(board[row][col])
        except ValueError:
          raise ValueError('NaN')
        if e <1 or e >9:
          raise ValueError('Invalid number.')

        b_row, b_col = get_block_coords((row, col))
        # checks the row map, the col map, and the block map
        if row_maps[row][e] ==1 or col_maps[col][e] ==1 or block_maps[b_row][b_col] == 1  :
          return False
        
        # updates the corresponding spot of each map.
        row_maps[row][e] += 1
        col_maps[col][e] += 1
        block_maps[b_row][b_col] += 1
  return True



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

print(bf_validate_sudoku(board))

print(bf_validate_sudoku(board))