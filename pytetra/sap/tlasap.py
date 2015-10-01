from .sap import Sap
from .primitive import Primitive


class TlaSap(Sap):
    pass


class TlUnitdataIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu
