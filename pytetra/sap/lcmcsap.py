from .sap import Sap
from .primitive import Primitive


class LcmcSap(Sap):
    pass


class MleUnitdataIndication(Primitive):
    def __init__(self, sdu):
        self.sdu = sdu
