from .sap import Sap


class UpperTlaSap(Sap):
    def tl_unitdata_indication(self, sdu):
        pass
