#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField, BitsField

# 21.4.1 MAC PDU types
class MacPdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 2),
    ]

    @classmethod
    def parse(cls, bits):
        pdu = super(MacPdu, cls).parse(bits)
        if pdu['pdu_type'] == 0:
            pdu.update(BroadcastPdu.parse(bits))
        return pdu

# 21.4.4 TMB-SAP: MAC PDU structure for broadcast   
class BroadcastPdu(Pdu):
    fields_desc = [
        UIntField("broadcast_type", 2),
    ]

    @classmethod
    def parse(cls, bits):
        pdu = super(BroadcastPdu, cls).parse(bits)
        return pdu

# 21.4.4.2 SYNC
class SyncPdu(Pdu):
    fields_desc = [
        UIntField("system_code", 4),
        UIntField("colour_code", 6),
        UIntField("timeslot_number", 2),
        UIntField("frame_number", 5),
        UIntField("multiframe_number", 6),
        UIntField("sharing_mode", 2),
        UIntField("ts_rsvd_frames", 3),
        UIntField("uplane_dtx", 1),
        UIntField("frame18_ext", 1),
        UIntField("reserved", 1),
        BitsField("tm_sdu", 29),
    ]

# 21.4.7 MAC PDU structure for access assignment broadcast
class AccessAssignPdu(Pdu):
    fields_desc = [
        UIntField("header", 2),
        UIntField("field1", 6),
        UIntField("field2", 6),
    ]

