from pytetra.layer.mac.pdu import MacPdu, NullPdu, SyncPdu, AccessAssignPdu, SysinfoPdu
from pytetra.layer.mac.decoder import SCHFDecoder, SCHHDDecoder, STCHDecoder, BSCHDecoder, AACHDecoder
from pytetra.sap.tpsap import TpSBIndication, TpNDBIndication
from pytetra.sap.tmvsap import TmvUnidataIndication
from pytetra.sap.tmasap import TmaUnitdataIndication
from pytetra.sap.tmbsap import TmbSyncIndication, TmbSysinfoIndication
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
        
        self.decoder = {}
        self.decoder['SCH/F'] = SCHFDecoder()
        self.decoder['SCH/HD'] = SCHHDDecoder()
        self.decoder['STCH'] = STCHDecoder()
        self.decoder['BSCH'] = BSCHDecoder()
        self.decoder['AACH'] = AACHDecoder()
        
    def recv(self, prim):
        if isinstance(prim, TpSBIndication):
            self.decodeBSCH(prim.SB)
            self.decodeAACH(prim.BB)
            self.decodeSCHHD(prim.BKN2)
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

    def getScramblingCode(self):
        return map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code))

    def decodeSCHF(self, b5):
        b1, crc_pass = self.decoder['SCH/F'].decode(b5, self.getScramblingCode())

        prim = TmvUnidataIndication(b1, "SCH/F", crc_pass)
        self.tmvsap.send(prim)

    def decodeSCHHD(self, b5):
        b1, crc_pass = self.decoder['SCH/HD'].decode(b5, self.getScramblingCode())
        
        prim = TmvUnidataIndication(b1, "SCH/HD", crc_pass)
        self.tmvsap.send(prim)

    def decodeTCH(self, b5):
        pass

    def decodeSTCH(self, b5):
        b1, crc_pass = self.decoder['STCH'].decode(b5, self.getScramblingCode())
        
        prim = TmvUnidataIndication(b1, "STCH", crc_pass)
        self.tmvsap.send(prim)

    def decodeBSCH(self, b5):
        b1, crc_pass = self.decoder['BSCH'].decode(b5, [0]*30)
        
        prim = TmvUnidataIndication(b1, "BSCH", crc_pass)
        self.tmvsap.send(prim)

    def decodeAACH(self, b5):
        b1, crc_pass = self.decoder['AACH'].decode(b5, self.getScramblingCode())
        
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
                    if isinstance(pdu, MacPdu):
                        self.warning('Unknown Mac PDU type')
                    else:
                        if isinstance(pdu, SysinfoPdu):
                            prim2 = TmbSysinfoIndication(pdu.sdu)
                            self.tmbsap.send(prim2)
                        else:
                            prim2 = TmaUnitdataIndication(pdu.sdu)
                            self.tmasap.send(prim2)
                
