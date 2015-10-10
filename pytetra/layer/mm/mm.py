from pytetra.layer.mm.pdu import MmPdu
from pytetra.sap.lmmsap import UpperLmmSap
from pytetra.layer import Layer


class Mm(Layer, UpperLmmSap):
    def mle_unitdata_indication(self, sdu):
        pdu = MmPdu.parse(sdu)
        self.info("%s" % (repr(pdu, )))
