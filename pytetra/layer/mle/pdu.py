#!/usr/bin/env python

# from pytetra.pdu import Pdu, UIntField, BitsField
from pytetra.pdu.sublayer32pdu import Pdu, Type1, Type2, Type3, PduDiscriminator, Repeat
from pytetra.layer.mle.elements import *


# 18.4.2.1 D-MLE-SYNC
class DMleSyncPdu(Pdu):
    name = "D-MLE-SYNC"
    type1 = [
        Type1(Mcc),
        Type1(Mnc),
        Type1(NeighbourCellBroadcast),
        Type1(CellServiceLevel),
        Type1(LateEntrySupported),
    ]
    type2 = []
    type34 = []
    has_o_bit = False


# 18.4.2.2 D-MLE-SYSINFO
class DMleSysinfoPdu(Pdu):
    name = "D-MLE-SYSINFO"
    type1 = [
        Type1(La),
        Type1(SubscriberClass),
        Type1(BsServiceDetails),
    ]
    type2 = []
    type34 = []
    has_o_bit = False


# 18.4.1.3 MLE service user PDUs
class MleServicePdu(Pdu):
    name = "MLE PDU"
    type1 = [
        Type1(ProtocolDiscriminator),
    ]
    type2 = []
    type34 = []
    sdu = True
    has_o_bit = False


# 18.4.1.4.1 D-NWRK-BROADCAST
class DNwrkBroadcast(Pdu):
    name = "D-NWRK-BROADCAST"
    type1 = [
        Type1(PduType),
        Type1(CellReselectParameters),
        Type1(CellServiceLevel),
    ]
    type2 = [
        Type2(TetraNetworkTime),
        Type2(NumberOfNeighbourCells),
        Repeat(NeighbourCellInformation, lambda pkt: pkt[NumberOfNeighbourCells].value),
    ]
    type34 = []


# 18.4.1.4.4 D-RESTORE-ACK
class DRestoreAck(Pdu):
    name = "D-RESTORE-ACK"
    type1 = [
        Type1(PduType),
    ]
    type2 = []
    type34 = []
    sdu = True


# 18.4.1.2 PDU type
class MlePdu(PduDiscriminator):
    element = PduType
    pdu_types = {
        2: DNwrkBroadcast,
        4: DRestoreAck,
    }
