from pytetra.layer.phy import Phy
from pytetra.layer.mac import LowerMac, UpperMac
from pytetra.layer.llc import Llc
from pytetra.layer.mle import Mle
from pytetra.layer.cmce import Cmce
from pytetra.sap.tpsap import TpSap
from pytetra.sap.tmvsap import TmvSap
from pytetra.sap.tmasap import TmaSap
from pytetra.sap.tmbsap import TmbSap
from pytetra.sap.tlasap import TlaSap
from pytetra.sap.tlbsap import TlbSap
from pytetra.sap.lcmcsap import LcmcSap


class TetraStack:
    def __init__(self):
        self.tpsap = TpSap()
        self.tmvsap = TmvSap()
        self.tmasap = TmaSap()
        self.tmbsap = TmbSap()
        self.tlasap = TlaSap()
        self.tlbsap = TlbSap()
        self.lcmcsap = LcmcSap()

        self.phy = Phy(self.tpsap)
        self.lower_mac = LowerMac(self.tpsap, self.tmvsap)
        self.upper_mac = UpperMac(self.tmvsap, self.tmasap, self.tmbsap)
        self.lower_mac.upper = self.upper_mac  # TODO : fix
        self.upper_mac.lower = self.lower_mac  # TODO : fix
        self.llc = Llc(self.tmasap, self.tmbsap, self.tlasap, self.tlbsap)
        self.mle = Mle(self.tlasap, self.tlbsap, self.lcmcsap)
        self.cmce = Cmce(self.lcmcsap)
