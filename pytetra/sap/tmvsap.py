from pytetra.sap import Sap


class UpperTmvSap(Sap):
    def tmv_unitdata_indication(self, block, channel, crc_pass):
        pass
