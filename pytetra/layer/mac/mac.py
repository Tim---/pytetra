from pytetra.layer.mac.scrambling import BSCHScrambler, Scrambler
from pytetra.layer.mac.interleaving import BSCHInterleaver
from pytetra.layer.mac.puncturer import Puncturer_2_3
from pytetra.layer.mac.convolutional import TETRAConvolutionalEncoder
from pytetra.layer.mac.crc import TETRACRC
from pytetra.layer.mac.pdu import SyncPdu, AccessAssignPdu
from pytetra.layer.mac.rmcode import ReedMuller
from pytetra.sap.tpsap import TpUnidataIndication
from pytetra.sap.tmvsap import TmvUnidataIndication
from pytetra.sap.tmbsap import TmbSyncIndication

class LowerMac:
    def __init__(self, tpsap, tmvsap):
        self.tpsap = tpsap
        self.tmvsap = tmvsap
        tpsap.register(self)
        tmvsap.register(self)
        
        self.mcc = 1
        self.mnc = 1
        self.colour_code = 1

    def recv(self, prim):
        if isinstance(prim, TpUnidataIndication):
            if prim.channel == "BSCH":
                self.decodeBSCH(prim.block)
            elif prim.channel == "AACH":
                self.decodeAACH(prim.block)

    def decodeBSCH(self, b5):
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

    def decodeAACH(self, b5):
        # Uncrambling
        s = Scrambler(map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code)))
        b2 = b3 = b4 = list(s.unscramble(b5))
        
        # Reed Muller decode
        rm = ReedMuller()
        crc_pass = rm.check(b2)
        print crc_pass
        b1 = rm.decode(b2)
        
        prim = TmvUnidataIndication(b1, "AACH", crc_pass)
        self.tmvsap.send(prim)

class UpperMac:
    def __init__(self, tmvsap, tmbsap):
        self.tmvsap = tmvsap
        self.tmbsap = tmbsap
        tmvsap.register(self)
        tmbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TmvUnidataIndication) and prim.crc_pass:
            if prim.channel == "BSCH":
                pdu = SyncPdu.parse(prim.block)
                prim = TmbSyncIndication(pdu['tm_sdu'])
                self.tmbsap.send(prim)
            elif prim.channel == "AACH":
                pdu = AccessAssignPdu.parse(prim.block)
