from pytetra.layer.phy import Phy
from pytetra.layer.mac import LowerMac, UpperMac
from pytetra.layer.llc import Llc
from pytetra.layer.mle import Mle
from pytetra.sap.tpsap import TpSap
from pytetra.sap.tmvsap import TmvSap
from pytetra.sap.tmasap import TmaSap
from pytetra.sap.tmbsap import TmbSap
from pytetra.sap.tlbsap import TlbSap

class TetraStack:
    def __init__(self):
        self.tpsap = TpSap()
        self.tmvsap = TmvSap()
        self.tmasap = TmbSap()
        self.tmbsap = TmbSap()
        self.tlbsap = TlbSap()
        
        self.phy = Phy(self.tpsap)
        self.lower_mac = LowerMac(self.tpsap, self.tmvsap)
        self.upper_mac = UpperMac(self.tmvsap, self.tmasap, self.tmbsap)
        self.lower_mac.upper = self.upper_mac # TODO : fix
        self.llc = Llc(self.tmasap, self.tmbsap, self.tlbsap)
        self.mle = Mle(self.tlbsap)
