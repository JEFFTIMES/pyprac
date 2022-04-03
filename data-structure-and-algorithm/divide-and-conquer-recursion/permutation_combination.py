from pprint import pprint
def combination_gen(n, r):
    for i in range(len(n)):
        if r == 1:
            yield (n[i],)
        else:
            gen = combination_gen(n[i+1:],r-1)
            for next in gen:
                yield (n[i],) + next
                    
def combination(l, k):
    return list(combination_gen(l, k))


def permutation(array, r, res=[]):
    # reach the base condition r==1, return current array
    if r == 1:
        # print('base:',array)
        res.append([*array])
        return
    
    # print('top level permutation() called, <input array>:',array,'<r>:',r)
    
    # recursively calls itself to process the sub-array with r-1
    permutation(array, r-1, res)
    
    # swap elements and recursively process the swapped sub-array
    for i in range(r-1):
        
        # print('swap condition, <r=', r, '>, <i=', i,'>, array:', array)
        
        if r % 2 == 0:
            array[i], array[r-1] = array[r-1], array[i]
            # print('even r: array[',i,'] swapped with array[',r-1,']', array)
        else:
            array[0], array[r-1] = array[r-1], array[0]
            # print('odd r: array[',0,'] swapped with array[',r-1,']', array)
            
        
        # print('sub level permutation() called, <input array>:',array,'<r>:',r-1)
        
        # recursively calls itself to process the swapped sub-array
        permutation(array, r-1, res)
        


def test():
  comb = combination('abcdef',3)
  pprint(list(comb))

  perm=[]
  src = [1,2,3,4]
  permutation(src, len(src), perm)
  pprint(perm)

if __name__ == '__main__':
  test()