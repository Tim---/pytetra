from .sap import Sap
from .primitive import Primitive

class TpSap(Sap):
    pass

class TpSBIndication(Primitive):
    def __init__(self, SB, BB, BKN2):
        self.SB = SB
        self.BB = BB
        self.BKN2 = BKN2

class TpNDBIndication(Primitive):
    def __init__(self, BB, BKN1, BKN2):
        self.BB = BB
        self.BKN1 = BKN1
        self.BKN2 = BKN2

