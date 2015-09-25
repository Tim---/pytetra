from pytetra.sap.tlasap import TlUnitdataIndication
from pytetra.sap.tlbsap import TlSyncIndication
from .pdu import DMleSyncPdu

class Mle:
    def __init__(self, tlasap, tlbsap):
        self.tlasap = tlasap
        self.tlbsap = tlbsap
        tlasap.register(self)
        tlbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TlSyncIndication):
            pdu = DMleSyncPdu(prim.sdu)
        elif isinstance(prim, TlUnitdataIndication):
            print prim.sdu
