from pytetra.layer.cmce.pdu import CmcePdu


class Cmce:
    def __init__(self, lcmcsap):
        self.lcmcsap = lcmcsap
        lcmcsap.register(self)

    def recv(self, prim):
        pdu = CmcePdu(prim.sdu)
