from pytetra.layer.phy import Phy
from pytetra.layer.mac import LowerMac, UpperMac
from pytetra.layer.llc import Llc
from pytetra.layer.mle import Mle
from pytetra.layer.cmce import Cmce


class TetraStack:
    def __init__(self):
        self.phy = Phy(self)
        self.lower_mac = LowerMac(self)
        self.upper_mac = UpperMac(self)
        self.llc = Llc(self)
        self.mle = Mle(self)
        self.cmce = Cmce(self)
