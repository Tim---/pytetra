from pytetra.layer.mac.scrambling import BSCHScrambler, Scrambler
from pytetra.layer.mac.interleaving import BSCHInterleaver, SCHFInterleaver, HalfInterleaver
from pytetra.layer.mac.puncturer import Puncturer_2_3
from pytetra.layer.mac.convolutional import TETRAConvolutionalEncoder
from pytetra.layer.mac.crc import TETRACRC
from pytetra.layer.mac.pdu import MacPdu, NullPdu, SyncPdu, AccessAssignPdu
from pytetra.layer.mac.rmcode import ReedMuller
from pytetra.sap.tpsap import TpSBIndication, TpNDBIndication
from pytetra.sap.tmvsap import TmvUnidataIndication
from pytetra.sap.tmasap import TmaUnitdataIndication
from pytetra.sap.tmbsap import TmbSyncIndication
from pytetra.timebase import g_timebase

class LowerMac:
    def __init__(self, tpsap, tmvsap):
        self.tpsap = tpsap
        self.tmvsap = tmvsap
        tpsap.register(self)
        tmvsap.register(self)
        
        self.mcc = 1
        self.mnc = 1
        self.colour_code = 1
        
        self.bkn2_stolen = False
        
    def recv(self, prim):
        if isinstance(prim, TpSBIndication):
            self.decodeBSCH(prim.SB)
            self.decodeAACH(prim.BB)
            # TODO : bkn2
        elif isinstance(prim, TpNDBIndication):
            self.decodeAACH(prim.BB)
            if self.upper.mode == "signalling":
                if prim.SF == 0:
                    self.decodeSCHF(prim.BKN1 + prim.BKN2)
                else:
                    self.decodeSCHHD(prim.BKN1)
                    self.decodeSCHHD(prim.BKN2)
            elif self.upper.mode == "traffic":
                if prim.SF == 0:
                    self.decodeTCH(prim.BKN1 + prim.BKN2)
                else:
                    self.decodeSTCH(prim.BKN1)
                    if self.bkn2_stolen:
                        self.decodeSTCH(prim.BKN2)
                    else:
                        self.decodeTCH(prim.BKN2)
                    self.bkn2_stolen = False

    def decodeSCHF(self, b5):
        # Uncrambling
        s = Scrambler(map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code)))
        b4 = list(s.unscramble(b5))

        # Deinterleaving
        i = SCHFInterleaver()
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

        prim = TmvUnidataIndication(b1, "SCH/F", crc_pass)
        self.tmvsap.send(prim)

    def decodeSCHHD(self, b5):
        # Uncrambling
        s = Scrambler(map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code)))
        b4 = list(s.unscramble(b5))

        # Deinterleaving
        i = HalfInterleaver()
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

        prim = TmvUnidataIndication(b1, "SCH/HD", crc_pass)
        self.tmvsap.send(prim)

    def decodeTCH(self, b5):
        pass

    def decodeSTCH(self, b5):
        # Uncrambling
        s = Scrambler(map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code)))
        b4 = list(s.unscramble(b5))

        # Deinterleaving
        i = HalfInterleaver()
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

        prim = TmvUnidataIndication(b1, "STCH", crc_pass)
        self.tmvsap.send(prim)

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
        b1 = rm.decode(b2)
        
        prim = TmvUnidataIndication(b1, "AACH", crc_pass)
        self.tmvsap.send(prim)

class UpperMac:
    def __init__(self, tmvsap, tmasap, tmbsap):
        self.tmvsap = tmvsap
        self.tmasap = tmasap
        self.tmbsap = tmbsap
        tmvsap.register(self)
        tmasap.register(self)
        tmbsap.register(self)
       
        self.mode = "signalling"

    def recv(self, prim):
        if isinstance(prim, TmvUnidataIndication) and prim.crc_pass:
            if prim.channel == "BSCH":
                pdu = SyncPdu(prim.block)
                g_timebase.update(pdu.timeslot_number + 1, pdu.frame_number, pdu.multiframe_number)
                prim = TmbSyncIndication(pdu.tm_sdu)
                self.tmbsap.send(prim)
            elif prim.channel == "AACH":
                pdu = AccessAssignPdu(prim.block)

                # Traffic mode ?
                if g_timebase.fn != 18 and pdu.header != 0 and pdu.field1 > 3:
                    self.mode = "traffic"
                else:
                    self.mode = "signalling"
            elif prim.channel in ["SCH/F", "SCH/HD", "STCH"]:
                while True:
                    if len(prim.block) < 23:
                        break
                    pdu = MacPdu(prim.block)
                    if isinstance(pdu, NullPdu):
                        if pdu.length_indication == 62:
                            self.lower.bkn2_stolen = True
                        break
                    else:
                        prim2 = TmaUnitdataIndication(pdu.sdu)
                        self.tmasap.send(prim2)
                
