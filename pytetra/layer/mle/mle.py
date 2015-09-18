from pytetra.sap.tlbsap import TlSyncIndication
from .pdu import DMleSyncPdu

class Mle:
    def __init__(self, tlbsap):
        self.tlbsap = tlbsap
        tlbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TlSyncIndication):
            pdu = DMleSyncPdu.parse(prim.sdu)
            print pdu
