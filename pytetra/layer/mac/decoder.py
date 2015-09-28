from pytetra.layer.mac.scrambling import Scrambler
from pytetra.layer.mac.interleaving import BSCHInterleaver, SCHFInterleaver, HalfInterleaver
from pytetra.layer.mac.puncturer import Puncturer_2_3
from pytetra.layer.mac.convolutional import TETRAConvolutionalEncoder
from pytetra.layer.mac.crc import TETRACRC
from pytetra.layer.mac.rmcode import ReedMuller

class Decoder:
    def decode(self, b5, scrambling_code):
        # Uncrambling
        b4 = list(self.s.unscramble(b5, scrambling_code))

        # Deinterleaving
        b3 = self.i.deinterleave(b4)

        # Rate-compatible punctured convolutional codes
        b3dp = list(self.p.depuncture(b3))
        b2 = self.e.decode(b3dp)
        b2, tail = b2[:-4], b2[-4:]

        # CRC
        b1, crc = b2[:-16], b2[-16:]
        crc_pass = self.c.compute(b1) == crc
        
        return b1, crc_pass

class SCHFDecoder(Decoder):
    def __init__(self):
        self.s = Scrambler()
        self.i = SCHFInterleaver()
        self.p = Puncturer_2_3()
        self.e = TETRAConvolutionalEncoder()
        self.c = TETRACRC()

class SCHHDDecoder(Decoder):
    def __init__(self):
        self.s = Scrambler()
        self.i = HalfInterleaver()
        self.p = Puncturer_2_3()
        self.e = TETRAConvolutionalEncoder()
        self.c = TETRACRC()

class BSCHDecoder(Decoder):
    def __init__(self):
        self.s = Scrambler()
        self.i = BSCHInterleaver()
        self.p = Puncturer_2_3()
        self.e = TETRAConvolutionalEncoder()
        self.c = TETRACRC()

class AACHDecoder(Decoder):
    def __init__(self):
        self.s = Scrambler()
        self.rm = ReedMuller()

    def decode(self, b5, scrambling_code):
        b2 = b3 = b4 = list(self.s.unscramble(b5, scrambling_code))
        crc_pass = self.rm.check(b2)
        b1 = self.rm.decode(b2)
        
        return b1, crc_pass

STCHDecoder = SCHHDDecoder
