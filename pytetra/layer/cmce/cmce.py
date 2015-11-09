from pytetra.layer.cmce.pdu import CmcePdu, DConnect, DConnectAcknowledge, DRelease, DSetup, DStatus, DTxCeased, DTxGranted, DCallProceeding, DSdsData, DAlert
from pytetra.layer.cmce.elements import CallIdentifier
from pytetra.sap.lcmcsap import UpperLcmcSap
from pytetra.layer import Layer


# 11 Call Control (CC) service description
class CallControl(object):
    (STATE_UNDEFINED, STATE_SETUP) = range(2)

    def __init__(self):
        self.calls = {}

    def mle_unitdata_indication(self, pdu):
        call_id = pdu[CallIdentifier].value
        if isinstance(pdu, DSetup):
            self.calls[call_id] = self.STATE_SETUP
        if isinstance(pdu, DRelease):
            if call_id in self.calls:
                del self.calls[call_id]


# 12 Supplementary Services (SS) service description
class SupplementaryServices(object):
    def mle_unitdata_indication(self, pdu):
        pass


# 13 Short Data Service (SDS) service description
class ShortDataService(object):
    def mle_unitdata_indication(self, pdu):
        pass


class Cmce(Layer, UpperLcmcSap):
    def __init__(self, stack):
        super(Cmce, self).__init__(stack)
        self.cc = CallControl()
        self.ss = SupplementaryServices()
        self.sds = ShortDataService()

    def mle_unitdata_indication(self, sdu):
        pdu = CmcePdu.parse(sdu)

        if pdu.__class__ in [DAlert, DCallProceeding, DConnect, DConnectAcknowledge, DRelease, DSetup, DTxCeased, DTxGranted]:
            # CC sub-entity
            self.cc.mle_unitdata_indication(pdu)
        elif pdu.__class__ in []:
            # SS sub-entity
            self.ss.mle_unitdata_indication(pdu)
        elif pdu.__class__ in [DStatus, DSdsData]:
            # SDS sub-entity
            self.sds.mle_unitdata_indication(pdu)

        self.expose_pdu(pdu)
