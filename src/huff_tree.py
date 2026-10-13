
class node:
    def __init__(self,char,freq):
        self.char = char
        self.freq = freq
        self.ln = None
        self.rn = None

    ## Comparador
    def __lt__(self, other):
        return self.freq < other.freq

    def is_leaf(self) :
        return self.ln is None and self.rn is None
