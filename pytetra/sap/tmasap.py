from .sap import Sap


class UpperTmaSap(Sap):
    def tma_unitdata_indication(self, sdu):
        pass
