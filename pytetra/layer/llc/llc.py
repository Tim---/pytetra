from pytetra.sap.tmasap import UpperTmaSap
from pytetra.sap.tmbsap import UpperTmbSap
from pytetra.layer.llc.pdu import LlcPdu
from pytetra.layer import Layer


class Llc(Layer, UpperTmaSap, UpperTmbSap):
    def __init__(self, stack):
        self.stack = stack

    def tma_unitdata_indication(self, sdu):
        pdu = LlcPdu(sdu)
        if 'sdu' in pdu.fields:
            self.stack.mle.tl_unitdata_indication(pdu.sdu)

    def tmb_sync_indication(self, sdu):
        self.stack.mle.tl_sync_indication(sdu)

    def tmb_sysinfo_indication(self, sdu):
        self.stack.mle.tl_sysinfo_indication(sdu)
