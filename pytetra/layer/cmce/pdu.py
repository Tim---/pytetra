#!/usr/bin/env python

from pytetra.pdu import Pdu, TypedPdu, UIntField, BitsField

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
        #elif pdu.pdu_type == 6:
        #    return DRelease(bits)
        #elif pdu.pdu_type == 7:
        #    return DSetup(bits)

# 14.7.1.4 D-CONNECT
class DConnect(TypedPdu):
    type1 = [
        UIntField("call_identifier", 14),
        UIntField("call_timeout", 4),
        UIntField("hook_method_selection", 1),
        UIntField("simplex_duplex", 1),
        UIntField("tx_grant", 2),
        UIntField("tx_req_perm", 1),
        UIntField("call_ownership", 1),
    ]
    type2 = [
        UIntField("basic_service_infos", 8),
        UIntField("call_status", 3),
        UIntField("notification_indicator", 6),
    ]

# 14.7.1.9 D-RELEASE
class DRelease(TypedPdu):
    type1 = [
    ]

# 14.7.1.12 D-SETUP
class DSetup(TypedPdu):
    type1 = [
    ]

