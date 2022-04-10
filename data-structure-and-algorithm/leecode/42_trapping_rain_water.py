'''
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it is able to trap after raining.
                                           |||
                |||         |||            |||
                |||         ||||||   |||   |||
          |||   ||||||   |||||||||||||||||||||
        --------------------------------------

The above elevation map is represented by array [0,1,0,3,1,0,1,3,2,1,2,1,4 ]. In this case, 
14 units of rain water (blue section) are being trapped. Thanks Marcos for contributing this image!
'''


def trapping_rain_water(terrian):

  left, right = 0, len(terrian)-1
  
  # initializes the left wall
  while terrian[left] < terrian[left+1]:
    left +=1
  # initializes the right wall
  while terrian[right] < terrian[right-1]:
    right -=1
  
  #initializes the top, bottom and volume
  volume = 0
  bottom = 0
  top = min(terrian[left], terrian[right])

  while left < right:

    for block in range(left+1, right):
      if terrian[block] < top:
        volume += (top - max(bottom,terrian[block]))  # max(bottom, terrian[block]) to filter the under water mountain.
    
    # moves the walls, if left wall is lower
    bottom = top
    if terrian[left] < terrian[right]:
      left +=1
      while left<len(terrian)-1 and (terrian[left] < terrian[left+1] or terrian[left] < bottom) :
        left +=1
    else:
      right -=1
      while right > 1 and (terrian[right] < terrian[right-1] or terrian[right] < bottom):
        right -= 1
    
    # reset the top and bottom
    top = min(terrian[left], terrian[right])
    
  return volume


if __name__ == '__main__':

  terrian = [0,1,0,3,1,0,1,3,2,1,2,1,4]
  print(trapping_rain_water(terrian))