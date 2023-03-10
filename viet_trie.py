from typing import List, Iterable, Generator
import itertools
import os.path
import re


class VietTrie:
  def __init__(self) -> None:
    self.next = {}
    self.is_word = False


  # this function is created for efficiency purposes
  # Used for efficient sliding window approach to extract all words in a sentence
  def trail_depth(self, word_gen: Generator[str, None, None]) -> int:
    depth = 0
    max_depth = depth
    tmp = self
    for token in word_gen:
      if token not in tmp.next:
        return max_depth
      tmp = tmp.next[token]
      depth += 1
      max_depth = depth if tmp.is_word else max_depth

    return max_depth

  def extract_words(self, original: str) -> List[str]:
    sentences = [sentence for sentence in re.split('[!.?,]+', original)]
    words = []
    for sentence in sentences:
      tokens = [token for token in sentence.split(" ") if token != ""]
      if not tokens:
        continue
        
      i = 0
      # construct a sliding window iterator every iteration
      while i < len(tokens):
        # skip names and title
        tmp = i
        while tmp < len(tokens) and tokens[tmp][0].isupper():
          tmp += 1
        if tmp != i:
          words.append(" ".join(tokens[i:tmp]))
        i = tmp
        if i == len(tokens):
          break

        # extract words from dictionary
        word_gen = itertools.islice(tokens , i, len(tokens)) # sliding window iterator
        depth = max(1, self.trail_depth(word_gen))
        words.append(" ".join(tokens[i:i+depth]))
        i += depth

    return words


  def has_word(self, word: str) -> bool:
    tokens = word.split(" ")
    tmp = self
    for token in tokens:
      if token not in tmp.next:
        return False
      tmp = tmp.next[token]

    return tmp.is_word


  def add_word(self, word: str) -> None:
    tokens = word.lower().split(" ")
    tmp = self
    for token in tokens:
      if token not in tmp.next:
        tmp.next[token] = self.__class__() # a hack to make VietTrie singleton :)
      tmp = tmp.next[token]
    tmp.is_word = True

words = []
with open(os.path.join(os.path.dirname(__file__), "words.txt"), "r") as f:
  words = f.read().split("\n")

# a hack to make VietTrie singleton :)
VietTrie = VietTrie()

for word in words:
  VietTrie.add_word(word)



if __name__ == "__main__":
  print(f"VietTrie.has_word(????n b??) --> {VietTrie.has_word('????n b??')}")
  print(f"VietTrie.has_word(????n ??ng) --> {VietTrie.has_word('????n ??ng')}")
  print(f"VietTrie.has_word(english) --> {VietTrie.has_word('english')}")
  print(f"VietTrie.has_word(vi???t nam) --> {VietTrie.has_word('vi???t nam')}")
  print(f"Extract words from this sentence: thi??n nhi??n Vi???t Nam r???t l?? h??ng v?? -> {VietTrie.extract_words('thi??n nhi??n Vi???t Nam r???t l?? h??ng v??')}")
  print(f"Extract words from this sentence: m??y l??c n??o c??ng ?? a ?? ???i nh???c h???t c??? ?????u -> {VietTrie.extract_words('m??y l??c n??o c??ng ?? a ?? ???i nh???c h???t c??? ?????u')}")
  print(f"Extract words from this sentence: ch???y ch???m ?? ?? ?? ???ch -> {VietTrie.extract_words('ch???y ch???m ?? ?? ?? ???ch')}")
  print(f"Extract words from this sentence: t??i t??n l?? Ho??ng D??ng -> {VietTrie.extract_words('t??i t??n l?? Ho??ng D??ng')}")
  print(f"Extract words from this sentence: T??i t??n l?? Ho??ng D??ng -> {VietTrie.extract_words('T??i t??n l?? Ho??ng D??ng')}")
  print(f"Extract words from this sentence: HSBC l?? ng??n h??ng -> {VietTrie.extract_words('HSBC l?? ng??n h??ng')}")











