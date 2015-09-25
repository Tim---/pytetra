#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField, BitsField, ConditionalField

# 21.2.1 LLC PDU types
class LlcPdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 4),
    ]

    @classmethod
    def parse(cls, bits):
        pdu = super(LlcPdu, cls).parse(bits)
        if pdu['pdu_type'] == 0:
            pdu.update(BlADataPdu.parse(bits, False))
        if pdu['pdu_type'] == 2:
            pdu.update(BlUDataPdu.parse(bits, False))
        elif pdu['pdu_type'] == 3:
            pdu.update(BlAckPdu.parse(bits, False))
        return pdu

# 21.2.2.1 BL-ADATA
class BlADataPdu(Pdu):
    fields_desc = [
        UIntField("n_r", 1),
        UIntField("n_s", 1),
    ]

    @classmethod
    def parse(cls, bits, fcs):
        pdu = super(BlADataPdu, cls).parse(bits)
        return pdu

# 21.2.2.1 BL-UDATA
class BlUDataPdu(Pdu):
    fields_desc = [
    ]

    @classmethod
    def parse(cls, bits, fcs):
        pdu = super(BlUDataPdu, cls).parse(bits)
        return pdu

# 21.2.2.1 BL-ACK
class BlAckPdu(Pdu):
    fields_desc = [
        UIntField("n_r", 1),
    ]

    @classmethod
    def parse(cls, bits, fcs):
        pdu = super(BlAckPdu, cls).parse(bits)
        return pdu

