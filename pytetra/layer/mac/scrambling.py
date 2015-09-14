import operator
import itertools

class Scrambler:
    def __init__(self, e):
        self.p = e + [1, 1]
        self.c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    
    def scramble(self, bits):
        for b in bits:
            np = reduce(operator.xor, (self.c[i]*self.p[i] for i in range(0, 32)))
            yield b ^ np
            self.p = [np] + self.p[:-1]
    
    unscramble = scramble

class BSCHScrambler(Scrambler):
    def __init__(self):
        Scrambler.__init__(self, [0]*30)

if __name__ == "__main__":
    s = Scrambler([0]*30)
    print list(s.scramble([1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1,0 ,1, 0,0 ,1, 0, 1, 0]))
