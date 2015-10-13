#!/usr/bin/env python

from pytetra.pdu.sublayer32pdu import Pdu, Type1, Type2, Type3, PduDiscriminator
from pytetra.layer.mm.elements import *


class DLocationUpdateAccept(Pdu):
    name = "D-LOCATION UPDATE ACCEPT"

    type1 = [
        Type1(PduType),
        Type1(LocationUpdateAcceptType),
    ]
    type2 = [
        Type2(Ssi),
        Type2(AddressExtension),
        Type2(SubscriberClass),
        Type2(EnergySavingMode),
        Type2(ScchInformationAndDistributionOn18thFrame),
    ]
    type34 = [
        Type4(NewRegisteredArea),
        Type3(GroupIdentityLocationAccept),
        Type3(DefaultGroupAttachementLifetime),
        Type3(AuthenticationDownlink),
        Type3(Proprietary),
    ]


# 16.9.2.1 D-ATTACH/DETACH GROUP IDENTITY
class DAttachDetachGroupIdentity(Pdu):
    name = "D-ATTACH/DETACH GROUP IDENTITY"

    type1 = [
        Type1(PduType),
        Type1(GroupIdentityReport),
        Type1(GroupIdentityAcknowledgementRequest),
        Type1(GroupIdentityAttachDetachMode),
    ]
    type2 = []
    type34 = [
        Type3(Proprietary),
        Type3(GroupReportResponse),
        Type4(GroupIdentityDownlink),
    ]


# 16.9.2.2 D-ATTACH/DETACH GROUP IDENTITY ACKNOWLEDGEMENT
class DAttachDetachGroupIdentityAcknowledgement(Pdu):
    name = "D-ATTACH/DETACH GROUP IDENTITY ACKNOWLEDGEMENT"

    type1 = [
        Type1(PduType),
        Type1(GroupIdentityAcceptReject),
        Type1(Reserved),
    ]
    type2 = []
    type34 = [
        Type3(Proprietary),
        Type4(GroupIdentityDownlink),
    ]


# 16.10.39 PDU type
class MmPdu(PduDiscriminator):
    element = PduType
    pdu_types = {
        5: DLocationUpdateAccept,
        10: DAttachDetachGroupIdentity,
        11: DAttachDetachGroupIdentityAcknowledgement,
    }
