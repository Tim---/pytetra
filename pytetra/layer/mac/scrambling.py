from operator import xor, mul
from itertools import starmap, izip


class Scrambler(object):
    def __init__(self, e):
        c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        p = [1, 1] + list(reversed(e))
        for i in range(432):
            p.append(reduce(xor, starmap(mul, izip(reversed(p[-32:]), c))))
        self.p = p[32:]

    def unscramble(self, bits):
        return starmap(xor, izip(bits, self.p))
