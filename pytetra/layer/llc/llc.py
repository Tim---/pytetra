from pytetra.sap.tmasap import TmaUnitdataIndication
from pytetra.sap.tmbsap import TmbSyncIndication, TmbSysinfoIndication
from pytetra.sap.tlasap import TlUnitdataIndication
from pytetra.sap.tlbsap import TlSyncIndication, TlSysinfoIndication
from pytetra.layer.llc.pdu import LlcPdu


class Llc:
    def __init__(self, tmasap, tmbsap, tlasap, tlbsap):
        self.tmasap = tmasap
        self.tmbsap = tmbsap
        self.tlasap = tlasap
        self.tlbsap = tlbsap
        tmasap.register(self)
        tmbsap.register(self)
        tlasap.register(self)
        tlbsap.register(self)

    def recv(self, prim):
        if isinstance(prim, TmaUnitdataIndication):
            pdu = LlcPdu(prim.sdu)
            if 'sdu' in pdu.fields:
                prim = TlUnitdataIndication(pdu.sdu)
                self.tlasap.send(prim)
        elif isinstance(prim, TmbSyncIndication):
            prim = TlSyncIndication(prim.sdu)
            self.tlbsap.send(prim)
        elif isinstance(prim, TmbSysinfoIndication):
            prim = TlSysinfoIndication(prim.sdu)
            self.tlbsap.send(prim)
