#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField, BitsField


# 21.2.1 LLC PDU types
class LlcPdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 4),
    ]

    def __new__(cls, bits):
        pdu = super(LlcPdu, cls).__new__(cls, bits)
        super(LlcPdu, cls).__init__(pdu, bits)
        if pdu.pdu_type == 0:
            return BlADataPdu(bits)
        elif pdu.pdu_type == 1:
            return BlDataPdu(bits)
        elif pdu.pdu_type == 2:
            return BlUDataPdu(bits)
        elif pdu.pdu_type == 3:
            return BlAckPdu(bits)
        elif pdu.pdu_type == 10:
            return AlUDataPdu(bits)


# 21.2.2.1 BL-ACK
class BlAckPdu(Pdu):
    fields_desc = [
        UIntField("n_r", 1),
    ]


# 21.2.2.2 BL-ADATA
class BlADataPdu(Pdu):
    fields_desc = [
        UIntField("n_r", 1),
        UIntField("n_s", 1),
        BitsField("sdu"),
    ]


# 21.2.2.3 BL-DATA
class BlDataPdu(Pdu):
    fields_desc = [
        UIntField("n_s", 1),
        BitsField("sdu"),
    ]


# 21.2.2.4 BL-UDATA
class BlUDataPdu(Pdu):
    fields_desc = [
        BitsField("sdu"),
    ]


# 21.2.2.4 AL-UDATA
class AlUDataPdu(Pdu):
    fields_desc = [
        UIntField("final", 1),
        UIntField("n_s", 8),
        UIntField("s_s", 8),
        BitsField("sdu"),
    ]
