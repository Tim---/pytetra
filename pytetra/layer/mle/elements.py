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
