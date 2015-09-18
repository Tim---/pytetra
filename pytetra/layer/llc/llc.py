from pytetra.sap.tmbsap import TmbSyncIndication
from pytetra.sap.tlbsap import TlSyncIndication

class Llc:
    def __init__(self, tmbsap, tlbsap):
        self.tmbsap = tmbsap
        self.tlbsap = tlbsap
        tmbsap.register(self)
        tlbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TmbSyncIndication):
            prim = TlSyncIndication(prim.sdu)
            self.tlbsap.send(prim)
