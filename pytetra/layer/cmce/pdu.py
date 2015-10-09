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
        Type1(TxGrant),
        Type1(TxReqPerm),
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
        Type1(TxGrant),
        Type1(TxReqPerm),
        Type1(CallPriority),
    ]
    type2 = [
        Type2(NotificationIndicator),
        Type2(TemporaryAddress),
        Type2(CallingPartyTypeIdentifier),
        Type2(CallingPartyAddressSsi, cond=lambda pkt: pkt["calling_party_addr_ssi"]._value in [1, 2]),
        Type2(CallingPartyExtension, cond=lambda pkt: pkt["calling_party_addr_ssi"]._value == 2),
    ]
    type34 = [
        Type3(ExternalSubscriberNumber),
        Type3(Facility),
        Type3(DmMsAddress),
        Type3(Proprietary),
    ]


# 14.7.1.13 D-TX CEASED
class DTxCeased(Pdu):
    name = "D-TX CEASED"

    type1 = [
        Type1(PduType),
        Type1(CallIdentifier),
        Type1(TxReqPerm),
    ]
    type2 = [
        Type2(NotificationIndicator),
    ]
    type34 = [
        Type3(Facility),
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


# 14.8.28 PDU type
class CmcePdu(PduDiscriminator):
    element = PduType
    pdu_types = {
        1: DCallProceeding,
        2: DConnect,
        6: DRelease,
        7: DSetup,
        9: DTxCeased,
    }


if __name__ == "__main__":
    from pytetra.pdu.pdu import Bits

    bits = Bits('000100000000000011001110000000')
    print CmcePdu(bits)

    bits = Bits('00111000000000001100111000000010011000001001010000000000000000011001010')
    print CmcePdu(bits)

    bits = Bits('0011000000000000110011100100')
    print CmcePdu(bits)

    bits = Bits('010010000000000011000')
    print CmcePdu(bits)

    bits = Bits('0000100000000000110110000100')
    print CmcePdu(bits)
