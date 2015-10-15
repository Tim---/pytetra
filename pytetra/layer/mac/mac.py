from pytetra.layer.mac.pdu import MacPdu, NullPdu, SyncPdu, AccessAssignPdu, SysinfoPdu, MacResourcePdu, MacFrag, MacEnd
from pytetra.layer.mac.decoder import Decoders
from pytetra.layer.mac.defragmenter import MacDefragmenter
from pytetra.sap.tpsap import UpperTpSap
from pytetra.sap.tmvsap import UpperTmvSap
from pytetra.timebase import g_timebase
from pytetra.layer import Layer
from pytetra.pdu import Bits


class LowerMac(Layer, UpperTpSap):
    def __init__(self, stack):
        super(LowerMac, self).__init__(stack)

        self.mcc = 0
        self.mnc = 0
        self.colour_code = 0

        self.bkn2_stolen = False

        self.decoder = Decoders()

    def tp_sb_indication(self, sb, bb, bkn2):
        self.decode("BSCH", sb)
        self.decode("AACH", bb)
        self.decode("SCH/HD", bkn2)

    def tp_ndb_indication(self, bb, bkn1, bkn2, sf):
        self.decode("AACH", bb)
        if self.stack.upper_mac.downlink_usage_marker in [UpperMac.UMa, UpperMac.UMc]:
            # Common control
            if sf == 0:
                self.decode("SCH/F", bkn1 + bkn2)
            else:
                self.decode("SCH/HD", bkn1)
                self.decode("SCH/HD", bkn2)
        elif self.stack.upper_mac.downlink_usage_marker in UpperMac.Umt:
            # For now, assume TCH/S for traffic mode
            if sf == 0:
                self.decode("TCH/S normal", bkn1 + bkn2)
            else:
                self.decode("STCH", bkn1)
                if self.bkn2_stolen:
                    self.decode("STCH", bkn2)
                else:
                    self.decode("TCH/S stealing", bkn2)
                self.bkn2_stolen = False

    def set_mobile_codes(self, mcc, mnc):
        if mcc != self.mcc or mnc != self.mnc:
            self.mcc = mcc
            self.mnc = mnc
            self.decoder.set_extended_colour_code(self.getExtendedColourCode())

    def set_colour_code(self, colour_code):
        if colour_code != self.colour_code:
            self.colour_code = colour_code
            self.decoder.set_extended_colour_code(self.getExtendedColourCode())

    def getExtendedColourCode(self):
        return map(int, '{0:010b}{1:014b}{2:06b}'.format(self.mcc, self.mnc, self.colour_code))

    def decode(self, channel, b5):
        b1, crc_pass = self.decoder.decode(channel, b5)
        if channel in ['BSCH', 'SCH/F', 'SCH/HD', 'STCH', 'AACH']:
            self.stack.upper_mac.tmv_unitdata_indication(Bits(''.join(map(str, b1))), channel, crc_pass)
        elif channel == 'TCH/S normal':
            for frame in b1:
                self.stack.upper_mac.tmd_unitdata_indication(Bits(''.join(map(str, frame))), channel, crc_pass)
        elif channel == 'TCH/S stealing':
            self.stack.upper_mac.tmd_unitdata_indication(Bits(''.join(map(str, b1))), channel, crc_pass)


class UpperMac(Layer, UpperTmvSap):
    # 21.4.7 MAC PDU structure for access assignment broadcast
    UMx, UMa, UMc, UMr = xrange(4)
    Umt = xrange(4, 2 ** 6)

    def __init__(self, stack):
        super(UpperMac, self).__init__(stack)

        self.downlink_usage_marker = None
        self.defragmenter = MacDefragmenter()

    def tmv_unitdata_indication(self, block, channel, crc_pass):
        if channel == "AACH":
            if crc_pass:
                pdu = AccessAssignPdu(block)
                self.expose_pdu(pdu)

                if g_timebase.fn == 18:
                    self.downlink_usage_marker = self.UMc
                else:
                    if pdu.header == 0:
                        self.downlink_usage_marker = self.UMc
                    else:
                        self.downlink_usage_marker = pdu.field1
            else:
                self.downlink_usage_marker = self.UMx
        elif crc_pass:
            if channel == "BSCH":
                pdu = SyncPdu(block)
                self.expose_pdu(pdu)
                g_timebase.update(pdu.timeslot_number + 1, pdu.frame_number, pdu.multiframe_number)
                self.stack.lower_mac.set_colour_code(pdu.colour_code)
                self.stack.llc.tmb_sync_indication(pdu.tm_sdu)
            elif channel in ["SCH/F", "SCH/HD", "STCH"]:
                while True:
                    if len(block) < 23:
                        break
                    pdu = MacPdu(block)
                    if isinstance(pdu, NullPdu):
                        if pdu.length_indication == 62:
                            self.stack.lower_mac.bkn2_stolen = True
                        break
                    elif isinstance(pdu, SysinfoPdu):
                        self.stack.llc.tmb_sysinfo_indication(pdu.sdu)
                    elif isinstance(pdu, MacResourcePdu) or isinstance(pdu, MacFrag) or isinstance(pdu, MacEnd):
                        pdu = self.defragmenter.process_pdu(pdu)
                        if pdu:
                            self.expose_pdu(pdu)
                            if len(pdu.sdu):
                                self.stack.llc.tma_unitdata_indication(pdu.sdu)

    def tmd_unitdata_indication(self, block, channel, crc_pass):
        self.stack.user.speech_indication(block, not crc_pass, self.downlink_usage_marker)
