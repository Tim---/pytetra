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
        Type3(GroupIdendtityLocationAccept),
        Type3(DefaultGroupAttachementLifetime),
        Type3(AuthenticationDownlink),
        Type3(Proprietary),
    ]

# 16.10.39 PDU type
class MmPdu(PduDiscriminator):
    element = PduType
    pdu_types = {
        5: DLocationUpdateAccept
    }

if __name__ == "__main__":
    from pytetra.pdu.pdu import Bits

    bits = Bits('01010111000001010100000111010001101110000010011000000101110000100000000000000000000001001000')
    print MmPdu(bits)
