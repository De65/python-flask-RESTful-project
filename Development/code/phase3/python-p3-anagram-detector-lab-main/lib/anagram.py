class Anagram:
    def __init__(self, word):
        self.word = word
    
    def match(self, list):
        ret = []
        for el in list:
            if sorted(el) == sorted([letter for letter in self.word]):
                ret.append(el)
        return ret