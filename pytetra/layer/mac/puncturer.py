#!/usr/bin/env python


class Depuncturer(object):
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


class Depuncturer_2_3(Depuncturer):
    def __init__(self):
        super(Depuncturer_2_3, self).__init__(3, [1, 2, 5], lambda i: i)


class FastPuncturer_2_3(object):
    def depuncture(self, b3):
        i = 0
        while i < len(b3):
            yield b3[i]
            yield b3[i + 1]
            yield None
            yield None
            yield b3[i + 2]
            yield None
            yield None
            yield None
            i += 3

Depuncturer_2_3 = FastPuncturer_2_3

if __name__ == "__main__":
    bits = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0]

    p = Depuncturer_2_3()
    print list(p.depuncture(bits))
