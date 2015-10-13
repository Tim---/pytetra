from pytetra.layer.cmce.pdu import CmcePdu
from pytetra.sap.lcmcsap import UpperLcmcSap
from pytetra.layer import Layer


class Cmce(Layer, UpperLcmcSap):
    def mle_unitdata_indication(self, sdu):
        pdu = CmcePdu.parse(sdu)
        self.expose_pdu(pdu)
