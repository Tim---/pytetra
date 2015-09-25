import operator
import itertools

class Scrambler:
    def __init__(self):
        self.c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    
    def scramble(self, bits, e):
        p = e + [1, 1]
        for b in bits:
            np = reduce(operator.xor, (self.c[i]*p[i] for i in range(0, 32)))
            yield b ^ np
            p = [np] + p[:-1]
    
    unscramble = scramble

if __name__ == "__main__":
    s = Scrambler([0]*30)
    print list(s.scramble([1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1,0 ,1, 0,0 ,1, 0, 1, 0]))
