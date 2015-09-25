#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField, BitsField

# 18.4.2.1 D-MLE-SYNC
class DMleSyncPdu(Pdu):
    fields_desc = [
        UIntField("mcc", 10),
        UIntField("mnc", 14),
        UIntField("neighbour_cell_broadcast", 2),
        UIntField("cell_service_level", 2),
        UIntField("late_entry_information", 1),
    ]

# 18.4.1.2 PDU type
class MlePdu(Pdu):
    fields_desc = [
        UIntField("protocol_discriminator", 3),
        BitsField("sdu"),
    ]
