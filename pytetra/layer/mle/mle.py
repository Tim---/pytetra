from pytetra.sap.tlasap import UpperTlaSap
from pytetra.sap.tlbsap import UpperTlbSap
from pytetra.pdu.sublayer32pdu import SduElement
from pytetra.layer.mle.pdu import MlePdu, DMleSyncPdu, DMleSysinfoPdu
from pytetra.layer.mle.elements import Mcc, Mnc, ProtocolDiscriminator
from pytetra.layer import Layer


class Mle(Layer, UpperTlaSap, UpperTlbSap):
    def tl_unitdata_indication(self, sdu):
        pdu = MlePdu.parse(sdu)
        if pdu[ProtocolDiscriminator].value == 1:
            self.stack.mm.mle_unitdata_indication(pdu[SduElement].value)
        elif pdu[ProtocolDiscriminator].value == 2:
            self.stack.cmce.mle_unitdata_indication(pdu[SduElement].value)

    def tl_sync_indication(self, sdu):
        pdu = DMleSyncPdu.parse(sdu)
        self.stack.lower_mac.set_mobile_codes(pdu[Mcc].value, pdu[Mnc].value)
        self.info("%s" % (repr(pdu, )))

    def tl_sysinfo_indication(self, sdu):
        pdu = DMleSysinfoPdu.parse(sdu)
        self.info("%s" % (repr(pdu, )))
