#!/usr/bin/env python

from pytetra.pdu import Pdu, UIntField, BitsField, ConditionalField

# 21.4.1 MAC PDU types
class MacPdu(Pdu):
    fields_desc = [
        UIntField("pdu_type", 2),
    ]

    @classmethod
    def parse(cls, direction, bits):
        pdu = super(MacPdu, cls).parse(bits)
        if pdu['pdu_type'] == 0:
            if direction == "downlink":
                pdu.update(MacResourcePdu.parse(bits))
        elif pdu['pdu_type'] == 2:
            print "Broadcast"
            pdu.update(BroadcastPdu.parse(bits))
        else:
            print "Mac PDU ?", pdu['pdu_type']
        return pdu

# 21.4.3.1 MAC-RESOURCE
class MacResourcePdu(Pdu):
    fields_desc = [
        UIntField("fill_bits_indication", 1),
        UIntField("position_of_grant", 1),
        UIntField("encryption_mode", 2),
        UIntField("random_access_flag", 1),
        UIntField("length_indication", 6),
        UIntField("address_type", 3),
        ConditionalField(UIntField("ssi", 24), lambda pkt: pkt['address_type'] in [1, 3, 4, 5, 6, 7]),
        ConditionalField(UIntField("event_label", 10), lambda pkt: pkt['address_type'] in [2, 5, 7]),
        ConditionalField(UIntField("usage_marker", 6), lambda pkt: pkt['address_type'] in [6]),
        UIntField("power_control_flag", 1),
        ConditionalField(UIntField("power_control_element", 4), lambda pkt: pkt['power_control_flag']),
        UIntField("slot_granting_flag", 1),
        ConditionalField(UIntField("slot_granting_element", 8), lambda pkt: pkt['power_control_flag']),
        UIntField("channel_allocation_flag", 1),
        ConditionalField(UIntField("allocation_type", 2), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("timeslot_assigned", 4), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("up_down_assigned", 2), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("clch_permission", 1), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("cell_change", 1), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("carrier_number", 12), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("ext_carrier_number", 1), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("freq_band", 4), lambda pkt: pkt['channel_allocation_flag'] and pkt['ext_carrier_number']),
        ConditionalField(UIntField("offset", 2), lambda pkt: pkt['channel_allocation_flag'] and pkt['ext_carrier_number']),
        ConditionalField(UIntField("duplex_spacing", 3), lambda pkt: pkt['channel_allocation_flag'] and pkt['ext_carrier_number']),
        ConditionalField(UIntField("reverse_operation", 1), lambda pkt: pkt['channel_allocation_flag'] and pkt['ext_carrier_number']),
        ConditionalField(UIntField("monitoring_pattern", 2), lambda pkt: pkt['channel_allocation_flag']),
        ConditionalField(UIntField("frame_18_monitoring_pattern", 2), lambda pkt: pkt['channel_allocation_flag'] and pkt['monitoring_pattern'] == 0),
    ]

    @classmethod
    def parse(cls, bits):
        initialSize = len(bits) + 2
        pdu = super(MacResourcePdu, cls).parse(bits)
        if 4 <= pdu['length_indication'] <= 34:
            sduSize = pdu['length_indication'] * 8 - (initialSize - len(bits))
            pdu['sdu'] = BitsField('sdu', sduSize).dissect(pdu, bits)
        # TODO : fragmentation and STCH
        return pdu

# 21.4.4 TMB-SAP: MAC PDU structure for broadcast   
class BroadcastPdu(Pdu):
    fields_desc = [
        UIntField("broadcast_type", 2),
    ]

    @classmethod
    def parse(cls, bits):
        pdu = super(BroadcastPdu, cls).parse(bits)
        if pdu['broadcast_type'] == 0:
            print "SYSINFO"
            pdu.update(SysinfoPdu.parse(bits))
        elif pdu['broadcast_type'] == 0:
            print "ACCESS DEFINE"
            #pdu.update(AccessDefinePdu.parse(bits))
        return pdu

# 21.4.4.1 SYSINFO
class SysinfoPdu(Pdu):
    fields_desc = [
        UIntField("main_carrier", 12),
        UIntField("frequency_band", 4),
        UIntField("offset", 2),
        UIntField("duplex_spacing", 3),
        UIntField("reverse_operation", 1),
        UIntField("number_of_scch", 2),
        UIntField("max_ms_txpwer", 3),
        UIntField("min_rxlevel", 4),
        UIntField("access_parameter", 4),
        UIntField("radio_downlink_timeout", 4),
        UIntField("hyperframe_or_cck", 1),
        ConditionalField(UIntField("hyperframe_number", 16), lambda pkt: pkt['hyperframe_or_cck'] == 0),
        ConditionalField(UIntField("cck", 16), lambda pkt: pkt['hyperframe_or_cck'] == 1),
        UIntField("optionnal_field", 2),
        ConditionalField(UIntField("ts_common_frames", 20), lambda pkt: pkt['optionnal_field'] in [0, 1]),
        ConditionalField(UIntField("default_def_access_code_a", 20), lambda pkt: pkt['optionnal_field'] == 2),
        ConditionalField(UIntField("extended_services", 20), lambda pkt: pkt['optionnal_field'] == 3),
        BitsField("sdu", 42),
    ]

    @classmethod
    def parse(cls, bits):
        pdu = super(SysinfoPdu, cls).parse(bits)
        if pdu['broadcast_type'] == 0:
            print "SYSINFO"
            #pdu.update(SysinfoPdu.parse(bits))
        elif pdu['broadcast_type'] == 0:
            print "ACCESS DEFINE"
            #pdu.update(AccessDefinePdu.parse(bits))
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

