#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField


class MmPdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 4),
    ]

    def __new__(cls, bits):
        pdu = super(MmPdu, cls).__new__(cls, bits)
        super(MmPdu, cls).__init__(pdu, bits)
