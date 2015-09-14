from .sap import Sap
from .primitive import Primitive

class TpSap(Sap):
    pass

class TpUnidataIndication(Primitive):
    def __init__(self, block, channel):
        self.block = block
        self.channel = channel
