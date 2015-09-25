from .sap import Sap
from .primitive import Primitive

class TmaSap(Sap):
    pass

class TmaUnitdataIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu

