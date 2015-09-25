from pytetra.sap.tmasap import TmaUnitdataIndication
from pytetra.sap.tmbsap import TmbSyncIndication
from pytetra.sap.tlbsap import TlSyncIndication
from pytetra.layer.llc.pdu import LlcPdu

class Llc:
    def __init__(self, tmasap, tmbsap, tlbsap):
        self.tmasap = tmasap
        self.tmbsap = tmbsap
        self.tlbsap = tlbsap
        tmasap.register(self)
        tmbsap.register(self)
        tlbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TmaUnitdataIndication):
            print prim.sdu[:4]
            pdu = LlcPdu.parse(prim.sdu)
        if isinstance(prim, TmbSyncIndication):
            prim = TlSyncIndication(prim.sdu)
            self.tlbsap.send(prim)
