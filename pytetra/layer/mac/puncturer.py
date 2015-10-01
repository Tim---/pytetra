#!/usr/bin/env python


class Puncturer:
    def __init__(self, t, P, f):
        self.t = t
        self.P = P
        self.f = f

    def depuncture(self, bits):
        v = [None] * (len(bits) * 8 / self.t)
        for j in range(len(bits)):
            i = self.f(j)
            k = 8 * (i / self.t) + self.P[i - self.t * (i / self.t)]
            v[k - 1] = bits[j]
        return v


class Puncturer_2_3(Puncturer):
    def __init__(self):
        Puncturer.__init__(self, 3, [1, 2, 5], lambda i: i)


class FastPuncturer_2_3:
    def depuncture(self, bits):
        i = 0
        while i < len(bits):
            yield bits[i]
            yield bits[i + 1]
            yield None
            yield None
            yield bits[i + 2]
            yield None
            yield None
            yield None
            i += 3

Puncturer_2_3 = FastPuncturer_2_3

if __name__ == "__main__":
    bits = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

    p = Puncturer_2_3()
    print list(p.depuncture(bits))
