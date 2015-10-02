
class BlockInterleaver(object):
    def __init__(self, K, a):
        self.K = K
        self.a = a

    def deinterleave(self, bits):
        return [bits[(self.a * (i + 1)) % self.K] for i in range(len(bits))]


class BSCHInterleaver(BlockInterleaver):
    def __init__(self):
        super(BSCHInterleaver, self).__init__(120, 11)


class SCHFInterleaver(BlockInterleaver):
    def __init__(self):
        super(SCHFInterleaver, self).__init__(432, 103)


class HalfInterleaver(BlockInterleaver):
    def __init__(self):
        super(HalfInterleaver, self).__init__(216, 101)
