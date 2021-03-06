from pytetra.sap.tlasap import UpperTlaSap
from pytetra.sap.tlbsap import UpperTlbSap
from pytetra.pdu.sublayer32pdu import SduElement
from pytetra.layer.mle.pdu import MlePdu, DMleSync, DMleSysinfo, MleServicePdu, DRestoreAck
from pytetra.layer.mle.elements import Mcc, Mnc, ProtocolDiscriminator
from pytetra.layer import Layer


class Mle(Layer, UpperTlaSap, UpperTlbSap):
    def tl_unitdata_indication(self, sdu):
        pdu = MleServicePdu.parse(sdu)

        if pdu[ProtocolDiscriminator].value == 'MM':
            self.stack.mm.mle_unitdata_indication(pdu[SduElement].value)
        elif pdu[ProtocolDiscriminator].value == 'CMCE':
            self.stack.cmce.mle_unitdata_indication(pdu[SduElement].value)
        elif pdu[ProtocolDiscriminator].value == 'MLE':
            pdu = MlePdu.parse(pdu[SduElement].value)
            self.expose_pdu(pdu)
            if isinstance(pdu, DRestoreAck):
                self.stack.cmce.mle_unitdata_indication(pdu[SduElement].value)
        else:
            raise NotImplementedError('Unknown MLE service : %s' % (pdu[ProtocolDiscriminator].value, ))

    def tl_sync_indication(self, sdu):
        pdu = DMleSync.parse(sdu)
        self.stack.lower_mac.set_mobile_codes(pdu[Mcc].value, pdu[Mnc].value)
        self.expose_pdu(pdu)

    def tl_sysinfo_indication(self, sdu):
        pdu = DMleSysinfo.parse(sdu)
        self.expose_pdu(pdu)
