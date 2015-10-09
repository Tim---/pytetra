from pytetra.pdu.sublayer32pdu import LeafElement, CompoundElement, Type1, Type2, Type4


class PduType(LeafElement):
    name = "PDU Type"
    length = 4


class LocationUpdateAcceptType(LeafElement):
    name = "Location update accept type"
    length = 3

    def value(self):
        return [
            "Roaming location updating",
            "Temporary registration",
            "Periodic location updating",
            "ITSI attach",
            "Call restoration roaming location updating",
            "Migrating or call restoration migrating location updating",
            "Demand location updating (D-Location Update command received)",
            "Disabled MS updating",
        ][self._value]


class Ssi(LeafElement):
    name = "SSI"
    length = 24


class Mcc(LeafElement):
    name = "MCC"
    length = 10


class Mnc(LeafElement):
    name = "MNC"
    length = 14


class AddressExtension(CompoundElement):
    name = "Address extension"

    type1 = [
        Type1(Mcc),
        Type1(Mnc),
    ]
    type2 = []
    type34 = []


class SubscriberClass(LeafElement):
    name = "Subscriber class"
    length = 16


class EnergySavingMode(LeafElement):
    name = "Energy saving mode"
    length = 3


class ScchInformation(LeafElement):
    name = "SCCH information"
    length = 4


class DistributionOn18thFrame(LeafElement):
    name = "Distribution on 18th frame"
    length = 2


class ScchInformationAndDistributionOn18thFrame(CompoundElement):
    name = "SCCH information and distribution on 18th frame"

    type1 = [
        Type1(ScchInformation),
        Type1(DistributionOn18thFrame),
    ]
    type2 = []
    type34 = []


class LaTimer(LeafElement):
    name = "LA timer"
    length = 3


class La(LeafElement):
    name = "LA"
    length = 14


class Lacc(LeafElement):
    name = "Location Area Country Code"
    length = 10


class Lanc(LeafElement):
    name = "Location Area Network Code"
    length = 14


class NewRegisteredArea(CompoundElement):
    name = "New registered area"
    identifier = 2

    type1 = [
        Type1(LaTimer),
        Type1(La),
    ]
    type2 = [
        Type2(Lacc, lambda elem: False),
        Type2(Lanc, lambda elem: False),
    ]
    type34 = []


class GroupIdentityAcceptReject(LeafElement):
    name = "Group identity accept/reject"
    length = 1

    def value(self):
        return ["accept", "reject"][self._value]


class Reserved(LeafElement):
    name = "Reserved"
    length = 1


class GroupIdentityAttachDetachTypeIdentifier(LeafElement):
    name = "Group identity attach/detach type identifier"
    length = 1

    def value(self):
        return ["attach", "detach"][self._value]


class GroupIdentityAttachmentLifetime(LeafElement):
    name = "Group identity attachment lifetime"
    length = 2


class ClassOfUsage(LeafElement):
    name = "Class of Usage"
    length = 3


class GroupIdentityAttachment(CompoundElement):
    name = "Group identity attachment"

    type1 = [
        Type1(GroupIdentityAttachmentLifetime),
        Type1(ClassOfUsage),
    ]
    type2 = []
    type34 = []


class GroupIdentityDetachmentDownlink(LeafElement):
    name = "Group identity detachment downlink"
    length = 2


class GroupIdentityAddressType(LeafElement):
    name = "Group identity address type"
    length = 2

    def value(self):
        return ["GSSI", "GTSI", "(V)GSSI", "GTSI+(V)GSSI"][self._value]


class Gssi(LeafElement):
    name = "GSSI"
    length = 24


class VGssi(LeafElement):
    name = "(V)GSSI"
    length = 24


class GroupIdentityDownlink(CompoundElement):
    name = "Group identity downlink"
    identifier = 7

    type1 = [
        Type1(GroupIdentityAttachDetachTypeIdentifier),
        Type1(GroupIdentityAttachment, cond=lambda elem: elem["Group identity attach/detach type identifier"].value() == "attach"),
        Type1(GroupIdentityDetachmentDownlink, cond=lambda elem: elem["Group identity attach/detach type identifier"].value() == "detach"),
        Type1(GroupIdentityAddressType),
        Type1(Gssi, cond=lambda elem: elem["Group identity address type"].value() in ["GSSI", "GTSI", "GTSI+(V)GSSI"]),
        Type1(AddressExtension, cond=lambda elem: elem["Group identity address type"].value() in ["GTSI", "GTSI+(V)GSSI"]),
        Type1(VGssi, cond=lambda elem: elem["Group identity address type"].value() in ["(V)GSSI", "GTSI+(V)GSSI"]),
    ]
    type2 = []
    type34 = []


class GroupIdendtityLocationAccept(CompoundElement):
    name = "Group identity location accept"
    identifier = 5

    type1 = [
        Type1(GroupIdentityAcceptReject),
        Type1(Reserved),
    ]
    type2 = []
    type34 = [
        Type4(GroupIdentityDownlink),
    ]


class DefaultGroupAttachementLifetime(LeafElement):
    name = "Default group attachment lifetime"
    length = 2


class AuthenticationDownlink(LeafElement):
    name = "Authentication Downlink"
    length = None  # TODO


class Proprietary(LeafElement):
    name = "Proprietary"
    length = None  # TODO
