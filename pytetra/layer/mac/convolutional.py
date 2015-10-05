#!/usr/bin/env python
# -*- coding: utf-8 -*-


# /!\ Inaccurate convolutional decoder /!\
class ConvolutionalDecoder(object):
    table = [
        [(0, 0), (1, 1)], [(3, 1), (2, 0)],
        [(4, 0), (5, 1)], [(7, 1), (6, 0)],
        [(8, 0), (9, 1)], [(11, 1), (10, 0)],
        [(12, 0), (13, 1)], [(15, 1), (14, 0)],
        [(1, 1), (0, 0)], [(2, 0), (3, 1)],
        [(5, 1), (4, 0)], [(6, 0), (7, 1)],
        [(9, 1), (8, 0)], [(10, 0), (11, 1)],
        [(13, 1), (12, 0)], [(14, 0), (15, 1)]
    ]

    def __init__(self, puncturer):
        self.puncturer = puncturer

    def __call__(self, b3):
        b3dp = list(self.puncturer.depuncture(b3))
        state = 0
        res = []
        for fb in b3dp[::4]:
            state, out = self.table[state][fb]
            res.append(out)
        return res[:-4]


if __name__ == "__main__":

    c = ConvolutionalDecoder()
    b2 = [1, 0, 1, 1, 0, 1, 0]
    v = list(c.encode(b2))
    print v
    print c.decode(v)
