
class BlockDeinterleaver(object):
    def __init__(self, K, a):
        self.K = K
        self.a = a
        self.shuffle = [(self.a * (i + 1)) % self.K for i in range(self.K)]

    def __call__(self, b4):
        return [b4[i] for i in self.shuffle]


class BSCHDeinterleaver(BlockDeinterleaver):
    def __init__(self):
        super(BSCHDeinterleaver, self).__init__(120, 11)


class SCHFDeinterleaver(BlockDeinterleaver):
    def __init__(self):
        super(SCHFDeinterleaver, self).__init__(432, 103)


class HalfDeinterleaver(BlockDeinterleaver):
    def __init__(self):
        super(HalfDeinterleaver, self).__init__(216, 101)
