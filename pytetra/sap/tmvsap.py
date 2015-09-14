from .sap import Sap
from .primitive import Primitive

class TmvSap(Sap):
    pass

class TmvUnidataIndication(Primitive):
    def __init__(self, block, channel, crc_pass):
        self.block = block
        self.channel = channel
        self.crc_pass = crc_pass
