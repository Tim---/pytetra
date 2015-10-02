from .sap import Sap


class UpperTpSap(Sap):
    def tp_sb_indication(self, sb, bb, bkn2):
        pass

    def tp_ndb_indication(self, bb, bkn1, bkn2, sf):
        pass
