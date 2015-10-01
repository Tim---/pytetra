from pytetra.sap.tlasap import TlUnitdataIndication
from pytetra.sap.tlbsap import TlSyncIndication, TlSysinfoIndication
from pytetra.sap.lcmcsap import MleUnitdataIndication
from pytetra.layer.mle.pdu import MlePdu
from .pdu import DMleSyncPdu, DMleSysinfoPdu


class Mle:
    def __init__(self, tlasap, tlbsap, lcmcsap):
        self.tlasap = tlasap
        self.tlbsap = tlbsap
        self.lcmcsap = lcmcsap
        tlasap.register(self)
        tlbsap.register(self)
        lcmcsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TlSyncIndication):
            pdu = DMleSyncPdu(prim.sdu)
        elif isinstance(prim, TlSysinfoIndication):
            pdu = DMleSysinfoPdu(prim.sdu)
        elif isinstance(prim, TlUnitdataIndication):
            pdu = MlePdu(prim.sdu)
            if pdu.protocol_discriminator == 2:
                prim = MleUnitdataIndication(pdu.sdu)
                self.lcmcsap.send(prim)
