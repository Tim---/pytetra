#!/usr/bin/env python

from itertools import cycle

class Puncturer:
    def __init__(self, t, P, f):
        self.t = t
        self.P = P
        self.f = f
        
    def depuncture(self, bits):
        v = [None] * (len(bits) * 8 / self.t)
        for j in range(len(bits)):
            i = self.f(j)
            k = 8 * (i/self.t) + self.P[i-self.t*(i/self.t)]
            v[k-1] = bits[j]
        return v

class Puncturer_2_3(Puncturer):
    def __init__(self):
        Puncturer.__init__(self, 3, [1, 2, 5], lambda i: i)

if __name__ == "__main__":
    p = Puncturer(3, [1, 2, 5], lambda i: i)
    print list(p.depuncture([0,0,1, 0,1,0 ,1,1,0, 1,0,1, 0,1,0]))
