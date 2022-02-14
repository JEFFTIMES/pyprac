from re import A
from urllib.request import Request, urlopen
from string import punctuation

war_and_peace = 'http://gutenberg.readingroo.ms/2/6/0/2600/2600.txt'
sherlock_holmes = "http://gutenberg.pglaf.org/1/6/6/1661/1661.txt"
peter_pan = 'https://www.gutenberg.org/files/16/16-0.txt'

def gutenberg(url):
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  res = urlopen(req)
  data = res.read()
  text = data.decode('utf-8')
  with open('gutenberg.txt', 'w') as f:
    f.write(text)
  words = ''.join([letter for letter in text if letter not in punctuation]).split()
  return text, words

def test():
  gutenberg(war_and_peace)


if __name__ == '__main__':
  test()

