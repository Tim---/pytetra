from operator import xor, mul
from itertools import starmap, izip


class Unscrambler(object):
    def __init__(self, extended_colour_code):
        c = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
        p = [1, 1] + list(reversed(extended_colour_code))
        for i in range(432):
            p.append(reduce(xor, starmap(mul, izip(reversed(p[-32:]), c))))
        self.p = p[32:]

    def __call__(self, b5):
        return list(starmap(xor, izip(b5, self.p)))
