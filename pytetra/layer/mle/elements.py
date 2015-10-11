from pytetra.pdu.sublayer32pdu import IntElement, EnumElement, CompoundElement, Type1, Type2, Type3


class ProtocolDiscriminator(IntElement):
    name = "Protocol discriminator"
    length = 3


class Mcc(IntElement):
    name = "MCC"
    length = 10


class Mnc(IntElement):
    name = "MNC"
    length = 14


class NeighbourCellBroadcast(IntElement):
    name = "Neighbour cell broadcast"
    length = 2


class CellServiceLevel(IntElement):
    name = "Cell service level"
    length = 2


class LateEntryInformation(IntElement):
    name = "Late entry information"
    length = 1


class La(IntElement):
    name = "LA"
    length = 14


class SubscriberClass(IntElement):
    name = "Subscriber class"
    length = 16


class BsServiceDetails(IntElement):
    name = "BS service details"
    length = 12
