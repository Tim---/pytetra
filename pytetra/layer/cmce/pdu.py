#!/usr/bin/env python

from pytetra.pdu import Pdu, TypedPdu, UIntField, Type1Field, Type2Field


# 14.8.28 PDU type
class CmcePdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 5),
    ]

    def __new__(cls, bits):
        pdu = super(CmcePdu, cls).__new__(cls, bits)
        super(CmcePdu, cls).__init__(pdu, bits)
        if pdu.pdu_type == 2:
            return DConnect(bits)
        elif pdu.pdu_type == 6:
            return DRelease(bits)
        elif pdu.pdu_type == 7:
            return DSetup(bits)
        elif pdu.pdu_type == 9:
            return DTxCeased(bits)


# 14.7.1.4 D-CONNECT
class DConnect(TypedPdu):
    type1 = [
        Type1Field("call_identifier", 14),
        Type1Field("call_timeout", 4),
        Type1Field("hook_method_selection", 1),
        Type1Field("simplex_duplex", 1),
        Type1Field("tx_grant", 2),
        Type1Field("tx_req_perm", 1),
        Type1Field("call_ownership", 1),
    ]
    type2 = [
        Type2Field("call_priority", 4),
        Type2Field("basic_service_infos", 8),
        Type2Field("temporary_address", 24),
        Type2Field("notification_indicator", 6),
    ]
    type3 = [
        Type2Field("facility", 3),
        Type2Field("proprietary", 15),
    ]
    type4 = [
    ]


# 14.7.1.9 D-RELEASE
class DRelease(TypedPdu):
    type1 = [
        Type1Field("call_identifier", 14),
        Type1Field("disconnect_cause", 5),
    ]
    type2 = [
        Type2Field("notification_indicator", 6),
    ]
    type3 = [
        Type2Field("facility", 3),
        Type2Field("proprietary", 15),
    ]
    type4 = [
    ]


# 14.7.1.12 D-SETUP
class DSetup(TypedPdu):
    type1 = [
        Type1Field("call_identifier", 14),
        Type1Field("call_timeout", 4),
        Type1Field("hook_method_selection", 1),
        Type1Field("simplex_duplex", 1),
        Type1Field("basic_service_infos", 8),
        Type1Field("tx_grant", 2),
        Type1Field("tx_req_perm", 1),
        Type1Field("call_priority", 4),
    ]
    type2 = [
        Type2Field("notification_indicator", 6),
        Type2Field("temporary_address", 24),
        Type2Field("calling_party_type_id", 2),
        Type2Field("calling_party_addr_ssi", 24, cond=lambda pkt: pkt.calling_party_type_id in [1, 2]),
        Type2Field("calling_party_extension", 24, cond=lambda pkt: pkt.calling_party_type_id == 2),
    ]
    type3 = [
        Type2Field("external_subscriber_number", 2),
        Type2Field("facility", 3),
        Type2Field("dm_ms_address", 6),
        Type2Field("proprietary", 15),
    ]
    type4 = [
    ]


# 14.7.1.13 D-TX CEASED
class DTxCeased(TypedPdu):
    type1 = [
        Type1Field("call_identifier", 14),
        Type1Field("tx_req_perm", 1),
    ]
    type2 = [
        Type2Field("notification_indicator", 6),
    ]
    type3 = [
        Type2Field("facility", 3),
        Type2Field("proprietary", 15),
    ]
    type4 = [
    ]


if __name__ == "__main__":
    # bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    # print DConnect(bits)
    # bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0]
    # print DSetup(bits)
    # bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]
    # print DRelease(bits)
    # bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    # print DTxCeased(bits)
    pass
