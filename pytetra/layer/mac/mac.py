from pytetra.layer.mac.pdu import MacPdu, NullPdu, SyncPdu, AccessAssignPdu, SysinfoPdu
from pytetra.layer.mac.decoder import SCHFDecoder, SCHHDDecoder, STCHDecoder, BSCHDecoder, AACHDecoder
from pytetra.sap.tpsap import UpperTpSap
from pytetra.sap.tmvsap import UpperTmvSap
from pytetra.timebase import g_timebase
from pytetra.layer import Layer


class LowerMac(Layer, UpperTpSap):
    def __init__(self, stack):
        super(LowerMac, self).__init__(stack)

        self.mcc = 1
        self.mnc = 1
        self.colour_code = 1

        self.bkn2_stolen = False

        self.decoder = {}
        self.decoder['SCH/F'] = SCHFDecoder(self.getExtendedColourCode())
        self.decoder['SCH/HD'] = SCHHDDecoder(self.getExtendedColourCode())
        self.decoder['STCH'] = STCHDecoder(self.getExtendedColourCode())
        self.decoder['BSCH'] = BSCHDecoder()
        self.decoder['AACH'] = AACHDecoder(self.getExtendedColourCode())

    def tp_sb_indication(self, sb, bb, bkn2):
        self.decodeBSCH(sb)
        self.decodeAACH(bb)
        self.decodeSCHHD(bkn2)

    def tp_ndb_indication(self, bb, bkn1, bkn2, sf):
        self.decodeAACH(bb)
        if self.stack.upper_mac.mode == "signalling":
            if sf == 0:
                self.decodeSCHF(bkn1 + bkn2)
            else:
                self.decodeSCHHD(bkn1)
                self.decodeSCHHD(bkn2)
        elif self.stack.upper_mac.mode == "traffic":
            if sf == 0:
                self.decodeTCH(bkn1 + bkn2)
            else:
                self.decodeSTCH(bkn1)
                if self.bkn2_stolen:
                    self.decodeSTCH(bkn2)
                else:
                    self.decodeTCH(bkn2)
                self.bkn2_stolen = False

    def getExtendedColourCode(self):
        return map(int, '{0:010b}{0:014b}{0:06b}'.format(self.mcc, self.mnc, self.colour_code))

    def decodeSCHF(self, b5):
        b1, crc_pass = self.decoder['SCH/F'].decode(b5)
        self.stack.upper_mac.tmv_unitdata_indication(b1, "SCH/F", crc_pass)

    def decodeSCHHD(self, b5):
        b1, crc_pass = self.decoder['SCH/HD'].decode(b5)
        self.stack.upper_mac.tmv_unitdata_indication(b1, "SCH/HD", crc_pass)

    def decodeTCH(self, b5):
        pass

    def decodeSTCH(self, b5):
        b1, crc_pass = self.decoder['STCH'].decode(b5)
        self.stack.upper_mac.tmv_unitdata_indication(b1, "STCH", crc_pass)

    def decodeBSCH(self, b5):
        b1, crc_pass = self.decoder['BSCH'].decode(b5)
        self.stack.upper_mac.tmv_unitdata_indication(b1, "BSCH", crc_pass)

    def decodeAACH(self, b5):
        b1, crc_pass = self.decoder['AACH'].decode(b5)
        self.stack.upper_mac.tmv_unitdata_indication(b1, "AACH", crc_pass)


class UpperMac(Layer, UpperTmvSap):
    def __init__(self, stack):
        super(UpperMac, self).__init__(stack)

        self.mode = "signalling"

    def tmv_unitdata_indication(self, block, channel, crc_pass):
        if crc_pass:
            if channel == "BSCH":
                pdu = SyncPdu(block)
                self.info("%s" % (repr(pdu, )))
                g_timebase.update(pdu.timeslot_number + 1, pdu.frame_number, pdu.multiframe_number)
                self.stack.llc.tmb_sync_indication(pdu.tm_sdu)
            elif channel == "AACH":
                pdu = AccessAssignPdu(block)
                self.info("%s" % (repr(pdu, )))

                # Traffic mode ?
                if g_timebase.fn != 18 and pdu.header != 0 and pdu.field1 > 3:
                    self.mode = "traffic"
                else:
                    self.mode = "signalling"
            elif channel in ["SCH/F", "SCH/HD", "STCH"]:
                while True:
                    if len(block) < 23:
                        break
                    pdu = MacPdu(block)
                    self.info("%s" % (repr(pdu, )))
                    if isinstance(pdu, NullPdu):
                        if pdu.length_indication == 62:
                            self.stack.lower_mac.bkn2_stolen = True
                        break
                    if isinstance(pdu, MacPdu):
                        self.warning('Unknown Mac PDU type')
                    else:
                        if isinstance(pdu, SysinfoPdu):
                            self.stack.llc.tmb_sysinfo_indication(pdu.sdu)
                        else:
                            self.stack.llc.tma_unitdata_indication(pdu.sdu)
