# given a series of number represents the prices of a stock in a duration,
# get the largest earning.

def max_stock_earn(prices):
  l = 0
  max_earning = 0
  h_index, l_index = 0, 0
  for i in range(len(prices)):
    if prices[i] < prices[l]:
      l = i
    earning = prices[i]-prices[l]
    if earning > max_earning:
      max_earning = earning
      h_index = i
      l_index = l 
  print(f'prices[{h_index}]={prices[h_index]},prices[{l_index}]={prices[l_index]}')  
  if l_index >= h_index:
    print('can not earn any money.')
  else:
    print(f'max earning: {prices[h_index]-prices[l_index]}')
  
def max_stock_earn2(prices):
  max_earning=0
  h, l = 0, 0
  lp = prices[0]
  for price in prices:
    if price < lp:
      lp = price
    earning = price - lp
    if earning > max_earning:
      max_earning = earning
      h = price
      l = lp
  print( max_earning, h, l)

if __name__ == '__main__':
  p1 = [9,11,8,5,7,12,16,14]
  p2 = [13,12,4,11,10,1,9]
  p3 = [10,9,8,7,5,1]
  max_stock_earn2(p1)
  max_stock_earn2(p2)
  max_stock_earn2(p3)