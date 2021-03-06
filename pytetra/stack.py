from pytetra.layer.phy import Phy
from pytetra.layer.mac import LowerMac, UpperMac
from pytetra.layer.llc import Llc
from pytetra.layer.mle import Mle
from pytetra.layer.cmce import Cmce
from pytetra.layer.mm import Mm
from pytetra.layer.user import UserLayer


class TetraStack(object):
    def __init__(self, user_class=UserLayer):
        self.phy = Phy(self)
        self.lower_mac = LowerMac(self)
        self.upper_mac = UpperMac(self)
        self.llc = Llc(self)
        self.mle = Mle(self)
        self.cmce = Cmce(self)
        self.mm = Mm(self)
        self.user = user_class(self)
