from pytetra.layer.mac.scrambling import BSCHScrambler
from pytetra.layer.mac.interleaving import BSCHInterleaver
from pytetra.layer.mac.puncturer import Puncturer_2_3
from pytetra.layer.mac.convolutional import TETRAConvolutionalEncoder
from pytetra.layer.mac.crc import TETRACRC
from pytetra.sap.tpsap import TpUnidataIndication
from pytetra.sap.tmvsap import TmvUnidataIndication

class LowerMac:
    def __init__(self, tpsap, tmvsap):
        self.tpsap = tpsap
        self.tmvsap = tmvsap
        tpsap.register(self)
        tmvsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TpUnidataIndication):
            self.decodeSB(prim.block)

    def decodeSB(self, b5):
        # Uncrambling
        s = BSCHScrambler()
        b4 = list(s.unscramble(b5))

        # Deinterleaving
        i = BSCHInterleaver()
        b3 = i.deinterleave(b4)

        # Rate-compatible punctured convolutional codes
        p = Puncturer_2_3()
        b3dp = p.depuncture(b3)
        c = TETRAConvolutionalEncoder()
        b2 = c.decode(b3dp)
        b2, tail = b2[:-4], b2[-4:]

        # CRC
        b1, crc = b2[:-16], b2[-16:]
        c = TETRACRC()
        crc_pass = c.compute(b1) == crc
        
        prim = TmvUnidataIndication(b1, "BSCH", crc_pass)
        self.tmvsap.send(prim)

class UpperMac:
    def __init__(self, tmvsap):
        self.tmvsap = tmvsap
        tmvsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TmvUnidataIndication):
            pass#print prim.block
