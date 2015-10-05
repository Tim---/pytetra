from pytetra.layer.mac.scrambling import Scrambler
from pytetra.layer.mac.interleaving import BSCHInterleaver, SCHFInterleaver, HalfInterleaver
from pytetra.layer.mac.puncturer import Puncturer_2_3
from pytetra.layer.mac.convolutional import TETRAConvolutionalEncoder
from pytetra.layer.mac.crc import TETRACRC
from pytetra.layer.mac.rmcode import ReedMuller


class Decoder(object):
    def decode(self, b5):
        # Uncrambling
        b4 = self.s.unscramble(b5)

        # Deinterleaving
        b3 = self.i.deinterleave(b4)

        # Rate-compatible punctured convolutional codes
        b2 = self.e.decode(b3)

        # CRC
        b1, crc_pass = self.c.compute(b2)

        return b1, crc_pass


class SCHFDecoder(Decoder):
    def __init__(self, scrambling_code):
        self.s = Scrambler(scrambling_code)
        self.i = SCHFInterleaver()
        self.e = TETRAConvolutionalEncoder(Puncturer_2_3())
        self.c = TETRACRC()


class SCHHDDecoder(Decoder):
    def __init__(self, scrambling_code):
        self.s = Scrambler(scrambling_code)
        self.i = HalfInterleaver()
        self.e = TETRAConvolutionalEncoder(Puncturer_2_3())
        self.c = TETRACRC()


class BSCHDecoder(Decoder):
    def __init__(self):
        self.s = Scrambler([0] * 30)
        self.i = BSCHInterleaver()
        self.e = TETRAConvolutionalEncoder(Puncturer_2_3())
        self.c = TETRACRC()


class AACHDecoder(Decoder):
    def __init__(self, scrambling_code):
        self.s = Scrambler(scrambling_code)
        self.rm = ReedMuller()

    def decode(self, b5):
        b2 = b3 = b4 = self.s.unscramble(b5)
        b1, crc_pass = self.rm.compute(b2)

        return b1, crc_pass

STCHDecoder = SCHHDDecoder
