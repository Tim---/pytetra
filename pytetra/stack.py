from pytetra.layer.phy import Phy
from pytetra.layer.mac import LowerMac, UpperMac
from pytetra.sap.tpsap import TpSap
from pytetra.sap.tmvsap import TmvSap

class TetraStack:
    def __init__(self):
        self.tpsap = TpSap()
        self.tmvsap = TmvSap()
        
        self.phy = Phy(self.tpsap)
        self.lower_mac = LowerMac(self.tpsap, self.tmvsap)
        self.upper_mac = UpperMac(self.tmvsap)
