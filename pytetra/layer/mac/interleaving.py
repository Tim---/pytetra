
class BlockInterleaver:
    def __init__(self, K, a):
        self.K = K
        self.a = a

    def deinterleave(self, bits):
        return [bits[(self.a*(i+1)) % self.K] for i in range(len(bits))]


class BSCHInterleaver(BlockInterleaver):
    def __init__(self):
        BlockInterleaver.__init__(self, 120, 11)


class SCHFInterleaver(BlockInterleaver):
    def __init__(self):
        BlockInterleaver.__init__(self, 432, 103)


class HalfInterleaver(BlockInterleaver):
    def __init__(self):
        BlockInterleaver.__init__(self, 216, 101)
