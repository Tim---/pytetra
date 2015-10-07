from pytetra.sap.tlasap import UpperTlaSap
from pytetra.sap.tlbsap import UpperTlbSap
from pytetra.layer.mle.pdu import MlePdu, DMleSyncPdu, DMleSysinfoPdu
from pytetra.layer import Layer


class Mle(Layer, UpperTlaSap, UpperTlbSap):
    def tl_unitdata_indication(self, sdu):
        pdu = MlePdu(sdu)
        self.info("%s" % (repr(pdu, )))
        if pdu.protocol_discriminator == 1:
            self.stack.mm.mle_unitdata_indication(pdu.sdu)
        if pdu.protocol_discriminator == 2:
            self.stack.cmce.mle_unitdata_indication(pdu.sdu)

    def tl_sync_indication(self, sdu):
        pdu = DMleSyncPdu(sdu)
        self.stack.lower_mac.set_mobile_codes(pdu.mcc, pdu.mnc)
        self.info("%s" % (repr(pdu, )))

    def tl_sysinfo_indication(self, sdu):
        pdu = DMleSysinfoPdu(sdu)
        self.info("%s" % (repr(pdu, )))
