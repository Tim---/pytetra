#!/usr/bin/env python

from pytetra.pdu.sublayer32pdu import Pdu, Type1, Type2, Type3, PduDiscriminator
from pytetra.layer.cmce.elements import *


# 14.7.1.4 D-CONNECT
class DConnect(Pdu):
    name = "D-CONNECT"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(CallTimeout),
        Type1(HookMethodSelection),
        Type1(SimplexDuplexSelection),
        Type1(TransmissionGrant),
        Type1(TransmissionRequestPermission),
        Type1(CallOwnership),
    ]
    type2 = [
        Type2(CallPriority),
        Type2(BasicServiceInformation),
        Type2(TemporaryAddress),
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.6 D-DISCONNECT
class DDisconnect(Pdu):
    name = "D-DISCONNECT"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(DisconnectCause),
    ]
    type2 = [
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.5 D-CONNECT ACKNOWLEDGE
class DConnectAcknowledge(Pdu):
    name = "D-CONNECT ACKNOWLEDGE"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(CallTimeout),
        Type1(TransmissionGrant),
        Type1(TransmissionRequestPermission),
    ]
    type2 = [
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.9 D-RELEASE
class DRelease(Pdu):
    name = "D-RELEASE"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(DisconnectCause),
    ]
    type2 = [
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.12 D-SETUP
class DSetup(Pdu):
    name = "D-SETUP"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(CallTimeout),
        Type1(HookMethodSelection),
        Type1(SimplexDuplexSelection),
        Type1(BasicServiceInformation),
        Type1(TransmissionGrant),
        Type1(TransmissionRequestPermission),
        Type1(CallPriority),
    ]
    type2 = [
        Type2(NotificationIndicator),
        Type2(TemporaryAddress),
        Type2(CallingPartyTypeIdentifier),
        Type2(CallingPartySsi, cond=lambda pkt: CallingPartyTypeIdentifier in pkt.fields and pkt[CallingPartyTypeIdentifier].value in ["SSI", "TSI"]),
        Type2(CallingPartyExtension, cond=lambda pkt: CallingPartyTypeIdentifier in pkt.fields and pkt[CallingPartyTypeIdentifier].value == "TSI"),
    ]
    type34 = [
        Type3(ExternalSubscriberNumber),
        Type3(Facility),
        Type3(DmMsAddress),
        Type3(Proprietary),
    ]


# 14.7.1.11 D-STATUS
class DStatus(Pdu):
    name = "D-STATUS"

    type1 = [
        Type1(PduType),
        Type1(CallingPartyTypeIdentifier),
        Type1(CallingPartySsi, cond=lambda pkt: pkt[CallingPartyTypeIdentifier].value in ["SSI", "TSI"]),
        Type1(CallingPartyExtension, cond=lambda pkt: pkt[CallingPartyTypeIdentifier].value == "TSI"),
        Type1(PrecodedStatus),
    ]
    type2 = []
    type34 = [
        Type3(ExternalSubscriberNumber),
        Type3(DmMsAddress),
    ]


# 14.7.1.13 D-TX CEASED
class DTxCeased(Pdu):
    name = "D-TX CEASED"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(TransmissionRequestPermission),
    ]
    type2 = [
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.15 D-TX GRANTED
class DTxGranted(Pdu):
    name = "D-TX GRANTED"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(TransmissionGrant),
        Type1(TransmissionRequestPermission),
        Type1(EncryptionControl),
        Type1(Reserved),
    ]
    type2 = [
        Type2(NotificationIndicator),
        Type2(TransmittingPartyTypeIdentifier),
        Type2(TransmittingPartySsi, cond=lambda pkt: pkt[TransmittingPartyTypeIdentifier].value in ["SSI", "TSI"]),
        Type2(TransmittingPartyExtension, cond=lambda pkt: pkt[TransmittingPartyTypeIdentifier].value == "TSI"),
    ]
    type34 = [
        Type3(ExternalSubscriberNumber),
        Type3(Facility),
        Type3(DmMsAddress),
        Type3(Proprietary),
    ]


# 14.7.1.2 D-CALL PROCEEDING
class DCallProceeding(Pdu):
    name = "D-CALL PROCEEDING"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(CallTimeoutSetUpPhase),
        Type1(HookMethodSelection),
        Type1(SimplexDuplexSelection),
    ]
    type2 = [
        Type2(BasicServiceInformation),
        Type2(CallStatus),
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.7.1.10 D-SDS-DATA
class DSdsData(Pdu):
    name = "D-SDS-DATA"

    type1 = [
        Type1(PduType),
        Type1(CallingPartyTypeIdentifier),
        Type1(CallingPartySsi, cond=lambda pkt: pkt[CallingPartyTypeIdentifier].value in ["SSI", "TSI"]),
        Type1(CallingPartyExtension, cond=lambda pkt: pkt[CallingPartyTypeIdentifier].value == "TSI"),
        Type1(ShortDataTypeIdentifier),
        Type1(UserDefinedData1, cond=lambda pkt: pkt[ShortDataTypeIdentifier].value == 0),
        Type1(UserDefinedData2, cond=lambda pkt: pkt[ShortDataTypeIdentifier].value == 1),
        Type1(UserDefinedData3, cond=lambda pkt: pkt[ShortDataTypeIdentifier].value == 2),
        Type1(LengthIndicator, cond=lambda pkt: pkt[ShortDataTypeIdentifier].value == 3),
        Type1(UserDefinedData4, cond=lambda pkt: pkt[ShortDataTypeIdentifier].value == 3, length_func=lambda pkt: pkt[LengthIndicator].value),
    ]
    type2 = []
    type34 = [
        Type3(ExternalSubscriberNumber),
        Type3(DmMsAddress),
    ]


# 14.7.1.1 D-ALERT
class DAlert(Pdu):
    name = "D-ALERT"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(CallTimeoutSetUpPhase),
        Type1(Reserved),
        Type1(SimplexDuplexSelection),
        Type1(CallQueued),
    ]
    type2 = [
        Type2(BasicServiceInformation),
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
        Type3(Proprietary),
    ]


# 14.8.28 PDU type
class CmcePdu(PduDiscriminator):
    element = PduType
    pdu_types = {
        1: DCallProceeding,
        2: DConnect,
        3: DConnectAcknowledge,
        4: DDisconnect,
        6: DRelease,
        7: DSetup,
        8: DStatus,
        9: DTxCeased,
        11: DTxGranted,
        15: DSdsData,
    }
