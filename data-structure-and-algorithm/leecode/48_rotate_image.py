'''
You are given an n x n 2D matrix representing an image.
Rotate the image by 90 degrees (clockwise).
Note:
You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Example 1:    
Given input matrix =
[
  [1,2,3],
  [4,5,6],
  [7,8,9]
],

'''

from typing import List, Tuple, Dict, Set

# turn the image upside down and exchange the numbers symmetric to the diagonal   
def rotate_image(img:List):
  image = list()
  for row in img:
    image.append(list(row))
  image.reverse()
  for row in range(len(image)):
    for col in range(row+1):
      image[row][col], image[col][row] = image[col][row], image[row][col]
  return image
  

# reverse each row of the image and exchange the numbers symmetric to the diagonal
def anticlock_rotate_image(img:List):
  image = list()
  for row in img:
    r = list(row)
    r.reverse()
    image.append(r)
  for row in range(len(image)):
    for col in range(row+1):
      image[row][col], image[col][row] = image[col][row], image[row][col]
  return image
  
if __name__ == '__main__':
  image = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
  ]
print( rotate_image(image) )

print(anticlock_rotate_image(image))