#!/usr/bin/env python

# from pytetra.pdu import Pdu, UIntField, BitsField
from pytetra.pdu.sublayer32pdu import Pdu, Type1, Type2, Type3, PduDiscriminator
from pytetra.layer.mle.elements import *


# 18.4.2.1 D-MLE-SYNC
class DMleSyncPdu(Pdu):
    name = "D-MLE-SYNC"
    type1 = [
        Type1(Mcc),
        Type1(Mnc),
        Type1(NeighbourCellBroadcast),
        Type1(CellServiceLevel),
        Type1(LateEntryInformation),
    ]
    type2 = []
    type34 = []


# 18.4.2.2 D-MLE-SYSINFO
class DMleSysinfoPdu(Pdu):
    name = "D-MLE-SYSINFO"
    type1 = [
        Type1(La),
        Type1(SubscriberClass),
        Type1(NeighbourCellBroadcast),
        Type1(BsServiceDetails),
    ]
    type2 = []
    type34 = []


# 18.4.1.2 PDU type
class MlePdu(Pdu):
    name = "MLE PDU"
    type1 = [
        Type1(ProtocolDiscriminator),
    ]
    type2 = []
    type34 = []
    sdu = True
