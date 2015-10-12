from pytetra.pdu.sublayer32pdu import IntElement, EnumElement, CompoundElement, Type1, Type2, Type3


# 18.5.21 Protocol discriminator
class ProtocolDiscriminator(EnumElement):
    name = "Protocol discriminator"
    length = 3
    enum = [
        "Reserved",
        "MM",
        "CMCE",
        "Reserved",
        "SNDCP",
        "MLE",
        "TETRA management entity protocol",
        "Testing",
    ]


# 18.5.20 PDU type
class PduType(EnumElement):
    name = "PDU type"
    length = 3
    enum = [
        "D-NEW CELL",
        "D-PREPARE FAIL",
        "D-NWRK-BROADCAST",
        "Reserved",
        "D-RESTORE-ACK",
        "D-RESTORE-FAIL",
        "Reserved",
        "Reserved",
    ]


# 18.5.4 Cell re-select parameters
class CellReselectParameters(IntElement):
    name = "Cell re-select parameters"
    length = 16


# 18.5.24 TETRA network time
class TetraNetworkTime(IntElement):
    name = "TETRA network time"
    length = 48


# 18.5.19 Number of neighbour cells
class NumberOfNeighbourCells(IntElement):
    name = "Number of neighbour cells"
    length = 3


# 18.5.14 MCC
class Mcc(IntElement):
    name = "MCC"
    length = 10


# 18.5.15 MNC
class Mnc(IntElement):
    name = "MNC"
    length = 14


# 18.5.16 Neighbour cell broadcast
class NeighbourCellBroadcast(IntElement):
    name = "Neighbour cell broadcast"
    length = 2


# 18.5.5 Cell service level
class CellServiceLevel(EnumElement):
    name = "Cell service level"
    length = 2
    enum = [
        "unknown",
        "low",
        "medium",
        "high",
    ]


# 18.5.8 Late entry supported
class LateEntrySupported(EnumElement):
    name = "Late entry supported"
    length = 1
    enum = [
        "unavailable",
        "available",
    ]


# 18.5.9 LA
class La(IntElement):
    name = "LA"
    length = 14


# 18.5.22 Subscriber class
class SubscriberClass(IntElement):
    name = "Subscriber class"
    length = 16


# 18.5.2 BS service details
class BsServiceRegistration(IntElement):
    name = "Registration"
    length = 1


class BsServiceDeregistration(IntElement):
    name = "De-registration"
    length = 1


class BsServicePriorityCell(IntElement):
    name = "Priority cell"
    length = 1


class BsServiceMinimumMode(IntElement):
    name = "Minimum mode service"
    length = 1


class BsServiceMigration(IntElement):
    name = "Migration"
    length = 1


class BsServiceSystemWide(IntElement):
    name = "System wide services"
    length = 1


class BsServiceTetraVoice(IntElement):
    name = "TETRA voice service"
    length = 1


class BsServiceCircuitModeData(IntElement):
    name = "Circuit mode data service"
    length = 1


class BsServiceReserved(IntElement):
    name = "Reserved"
    length = 1


class BsServiceSndcp(IntElement):
    name = "SNDCPService"
    length = 1


class BsServiceEncryption(IntElement):
    name = "Air interface encryption service"
    length = 1


class BsServiceAdvancedLink(IntElement):
    name = "Advanced link supported"
    length = 1


class BsServiceDetails(CompoundElement):
    name = "BS service details"
    type1 = [
        Type1(BsServiceRegistration),
        Type1(BsServiceDeregistration),
        Type1(BsServicePriorityCell),
        Type1(BsServiceMinimumMode),
        Type1(BsServiceMigration),
        Type1(BsServiceSystemWide),
        Type1(BsServiceTetraVoice),
        Type1(BsServiceCircuitModeData),
        Type1(BsServiceReserved),
        Type1(BsServiceSndcp),
        Type1(BsServiceEncryption),
        Type1(BsServiceAdvancedLink),
    ]
    type2 = []
    type34 = []


# 18.5.3 Cell identifier
class CellIdentifier(IntElement):
    name = "Cell identifier"
    length = 5


# 18.5.1 Cell re-selection types supported
class CellReselectionTypesSupported(IntElement):
    name = "Cell re-selection types supported"
    length = 2


# 18.5.18 Neighbour cell synchronized
class NeighbourCellSynchronized(IntElement):
    name = "Neighbour cell synchronized"
    length = 1


# 18.5.10 Main carrier number
class MainCarrierNumber(IntElement):
    name = "Main carrier number"
    length = 12


# 18.5.11 Main carrier number extension
class MainCarrierNumberExtension(IntElement):
    name = "Main carrier number extension"
    length = 10


# 18.5.13 Maximum MS transmit power
class MaximumMsTransmitPower(IntElement):
    name = "Maximum MS transmit power"
    length = 3


# 18.5.12 Minimum Rx access level
class MinimumRxAccessLevel(IntElement):
    name = "Minimum Rx access level"
    length = 4


# 18.5.25 Timeshare cell and AI encryption information
class TimeshareCellAndAiEncryptionInformation(IntElement):
    name = "Timeshare cell and AI encryption information"
    length = 5


# 18.5.23 TDMA frame offset
class TdmaFrameOffset(IntElement):
    name = "TDMA frame offset"
    length = 6


# 18.5.17 Neighbour cell information
class NeighbourCellInformation(CompoundElement):
    name = "Neighbour cell information"
    type1 = [
        Type1(CellIdentifier),
        Type1(CellReselectionTypesSupported),
        Type1(NeighbourCellSynchronized),
        Type1(CellServiceLevel),
        Type1(MainCarrierNumber),
    ]
    type2 = [
        Type2(MainCarrierNumberExtension),
        Type2(Mcc),
        Type2(Mnc),
        Type2(La),
        Type2(MaximumMsTransmitPower),
        Type2(MinimumRxAccessLevel),
        Type2(SubscriberClass),
        Type2(BsServiceDetails),
        Type2(TimeshareCellAndAiEncryptionInformation),
        Type2(TdmaFrameOffset),
    ]
    type34 = []
