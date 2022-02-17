from heapq import heapify, heappop, heappush
from operator import ge
from platform import node

from idna import encode

class Node():
  
  def __init__(self, probability=0, symbol=None, code='', left=None, right=None):
    self.symbol = symbol
    self.probability = probability
    self.left = left
    self.right = right
    self.code = code

  def set_code(self, code):
    self.code = code

  def __eq__(self, other):
        return (self.probability == other.probability) and (self.symbol == other.symbol)

  def __ne__(self, other):
      return not (self == other)

  def __lt__(self, other):
      return (self.probability < other.probability) and (self.symbol < other.symbol)

  def __gt__(self, other):
      return (self.probability > other.probability) and (self.symbol > other.symbol)

  def __le__(self, other):
      return (self < other) or (self == other)

  def __ge__(self, other):
      return (self > other) or (self == other)


class HuffmanCodec(object):
  
  def __init__(self, probabilities= None,):
    if not probabilities:
      self.probabilities = dict()
    else: 
      self.probabilities = probabilities
    self.bytes_repr = None
    self.tree = None
    self.encoding_map = dict()

  def convert_to_bytes(self, text, encoding):
    self.bytes_repr = text.encode(encoding)
    return self.bytes_repr

  def generate_prob_dict(self,):
    for byte in self.bytes_repr:
      try:
        self.probabilities[byte] += 1
      except KeyError:
        self.probabilities[byte] = 1
    # equivalent expression: self.probabilities = Counter(list(self.bytes_repr))
    return self.probabilities

  def generate_tree(self,):
    # create the heap from the probabilities
    heap = [ (probability, Node(probability=probability, symbol=byte)) for byte, probability in self.probabilities.items() ] 
    heapify(heap)
    # generate the tree
    while len(heap) > 1: 
      low = heappop(heap)
      high = heappop(heap)
      low[1].set_code('1')
      high[1].set_code('0')
      new_node = Node(probability=low[0]+high[0], left=high[1], right=low[1])
      heappush(heap,(new_node.probability, new_node))
    self.tree = heappop(heap)[1]
    return self.tree

  def generate_encoding_map(self, node, init_code=''):
    codec = init_code + node.code
    if not node.left and not node.right :
      self.encoding_map[node.symbol] = codec
      return
    else:
      self.generate_encoding_map(node.left, codec)
      self.generate_encoding_map(node.right, codec)
    return self.encoding_map

  def compress(self, text, encoding):
    # convert the text to bytes using the encoding specified
    self.convert_to_bytes(text, encoding)
  
    # generate the probability dictionary.
    self.generate_prob_dict()
    
    # generate huffman tree
    self.generate_tree()
    
    # generate encoding map 
    self.generate_encoding_map(self.tree)

    # convert the text to huffman encoded string
    encoded_string = ''.join([self.encoding_map[byte] for byte in self.bytes_repr])
    
    # entail the string to make the last byte is a whole byte.
    suffix_len = (8- (len(encoded_string) % 8)) 
    if suffix_len == 8:
      encoded_string = encoded_string + '0' * suffix_len
    
    # transfer the binary string to bytes
    compressed = bytes( [ int(encoded_string[i:i+8], 2) for i in range(0, len(encoded_string), 8) ] )
    
    return compressed, self.probabilities, suffix_len

  def decompress(self, compressed, encoding, probabilities=None, suffix=0 ):

    # generate the huffman tree
    if probabilities:
      self.probabilities = probabilities

    self.generate_tree()

    # convert the compressed bytes into binary string
    binary_string = ''.join([format(byte, '08b') for byte in compressed])
    if suffix !=0:
      binary_string = binary_string[:-suffix]
  
    # take the character one by one from the encoded string, walk through 
    # the tree and yield the symbol when reach a node with a symbol is not None,
    # then return to the tree root to continue.
    text = []
    node = self.tree
    count = 0
    for bit in binary_string:
      if bit == '0':
        node = node.left
      else:
        node = node.right
      count +=1
      if node.symbol:
        text += [node.symbol]
        node = self.tree

    return bytes(text).decode(encoding)

def test():

  text = '''  
  "Well, Prince, so Genoa and Lucca are now just family estates of the
Buonapartes. But I warn you, if you don't tell me that this means war,
if you still try to defend the infamies and horrors perpetrated by that
Antichrist--I really believe he is Antichrist--I will have nothing more
to do with you and you are no longer my friend, no longer my 'faithful
slave,' as you call yourself! But how do you do? I see I have frightened
you--sit down and tell me all the news."

It was in July, 1805, and the speaker was the well-known Anna Pavlovna
Scherer, maid of honor and favorite of the Empress Marya Fedorovna. With
these words she greeted Prince Vasili Kuragin, a man of high rank and
importance, who was the first to arrive at her reception. Anna Pavlovna
had had a cough for some days. She was, as she said, suffering from la
grippe; grippe being then a new word in St. Petersburg, used only by the
elite.

All her invitations without exception, written in French, and delivered
by a scarlet-liveried footman that morning, ran as follows:

"If you have nothing better to do, Count (or Prince), and if the
prospect of spending an evening with a poor invalid is not too terrible,
I shall be very charmed to see you tonight between 7 and 10--Annette
Scherer."

"Heavens! what a virulent attack!" replied the prince, not in the least
disconcerted by this reception. He had just entered, wearing an
embroidered court uniform, knee breeches, and shoes, and had stars on
his breast and a serene expression on his flat face. He spoke in that
refined French in which our grandfathers not only spoke but thought, and
with the gentle, patronizing intonation natural to a man of importance
who had grown old in society and at court. He went up to Anna Pavlovna,
kissed her hand, presenting to her his bald, scented, and shining head,
and complacently seated himself on the sofa.

"First of all, dear friend, tell me how you are. Set your friend's mind
at rest," said he without altering his tone, beneath the politeness and
affected sympathy of which indifference and even irony could be
discerned.

"Can one be well while suffering morally? Can one be calm in times like
these if one has any feeling?" said Anna Pavlovna. "You are staying the
whole evening, I hope?"
  '''
  encoding = 'utf-8'
  huffman = HuffmanCodec()
  compressed, prob, suffix = huffman.compress(text, encoding)
  print(f'compress rate: {len(compressed)/len(text)}\n')
  huffman2 = HuffmanCodec( probabilities=prob)
  text = huffman2.decompress(compressed, encoding, suffix=suffix)
  print(text)

if __name__ == '__main__':
  test()

