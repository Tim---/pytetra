from .sap import Sap
from .primitive import Primitive

class TmbSap(Sap):
    pass

class TmbSyncIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu

class TmbSysinfoIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu
