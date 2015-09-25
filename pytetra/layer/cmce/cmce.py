from pytetra.layer.cmce.pdu import CmcePdu, DConnect

class Cmce:
    def __init__(self, lcmcsap):
        self.lcmcsap = lcmcsap
        lcmcsap.register(self)

    def recv(self, prim):
        pdu = CmcePdu(prim.sdu)
        if isinstance(pdu, DConnect):
            print pdu
