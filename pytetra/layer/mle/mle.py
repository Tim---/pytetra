from pytetra.sap.tlasap import UpperTlaSap
from pytetra.sap.tlbsap import UpperTlbSap
from pytetra.layer.mle.pdu import MlePdu, DMleSyncPdu, DMleSysinfoPdu
from pytetra.layer import Layer


class Mle(Layer, UpperTlaSap, UpperTlbSap):
    def __init__(self, stack):
        self.stack = stack

    def tl_unitdata_indication(self, sdu):
            pdu = MlePdu(sdu)
            if pdu.protocol_discriminator == 2:
                self.stack.cmce.mle_unitdata_indication(pdu.sdu)

    def tl_sync_indication(self, sdu):
            pdu = DMleSyncPdu(sdu)

    def tl_sysinfo_indication(self, sdu):
            pdu = DMleSysinfoPdu(sdu)
