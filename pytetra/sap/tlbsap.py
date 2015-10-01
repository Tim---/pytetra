from .sap import Sap
from .primitive import Primitive


class TlbSap(Sap):
    pass


class TlSyncIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu


class TlSysinfoIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu
