from pytetra.pdu.sublayer32pdu import IntElement, EnumElement, CompoundElement, Type1, Type2, Type4


class PduType(IntElement):
    name = "PDU Type"
    length = 4


class LocationUpdateAcceptType(EnumElement):
    name = "Location update accept type"
    length = 3
    enum = [
        "Roaming location updating",
        "Temporary registration",
        "Periodic location updating",
        "ITSI attach",
        "Call restoration roaming location updating",
        "Migrating or call restoration migrating location updating",
        "Demand location updating (D-Location Update command received)",
        "Disabled MS updating"
    ]

class Ssi(IntElement):
    name = "SSI"
    length = 24


class Mcc(IntElement):
    name = "MCC"
    length = 10


class Mnc(IntElement):
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


class SubscriberClass(IntElement):
    name = "Subscriber class"
    length = 16


class EnergySavingMode(IntElement):
    name = "Energy saving mode"
    length = 3


class ScchInformation(IntElement):
    name = "SCCH information"
    length = 4


class DistributionOn18thFrame(IntElement):
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


class LaTimer(IntElement):
    name = "LA timer"
    length = 3


class La(IntElement):
    name = "LA"
    length = 14


class Lacc(IntElement):
    name = "Location Area Country Code"
    length = 10


class Lanc(IntElement):
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


class GroupIdentityAcceptReject(EnumElement):
    name = "Group identity accept/reject"
    length = 1
    enum = ["accept", "reject"]


class Reserved(IntElement):
    name = "Reserved"
    length = 1


class GroupIdentityAttachDetachTypeIdentifier(EnumElement):
    name = "Group identity attach/detach type identifier"
    length = 1
    enum = ["attach", "detach"]


class GroupIdentityAttachmentLifetime(IntElement):
    name = "Group identity attachment lifetime"
    length = 2


class ClassOfUsage(IntElement):
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


class GroupIdentityDetachmentDownlink(IntElement):
    name = "Group identity detachment downlink"
    length = 2


class GroupIdentityAddressType(EnumElement):
    name = "Group identity address type"
    length = 2
    enum = ["GSSI", "GTSI", "(V)GSSI", "GTSI+(V)GSSI"]


class Gssi(IntElement):
    name = "GSSI"
    length = 24


class VGssi(IntElement):
    name = "(V)GSSI"
    length = 24


# 16.10.26 Group identity report
class GroupIdentityReport(IntElement):
    name = "Group identity report"
    length = 1


# 16.10.13 Group identity acknowledgement request
class GroupIdentityAcknowledgementRequest(IntElement):
    name = "Group identity acknowledgement request"
    length = 1


# 16.10.17 Group identity attach/detach mode
class GroupIdentityAttachDetachMode(IntElement):
    name = "Group identity attach/detach mode"
    length = 1


# 16.10.27A Group report response
class GroupReportResponse(IntElement):
    name = "Group report response"
    identifier = 4
    length = 1


class GroupIdentityDownlink(CompoundElement):
    name = "Group identity downlink"
    identifier = 7

    type1 = [
        Type1(GroupIdentityAttachDetachTypeIdentifier),
        Type1(GroupIdentityAttachment, cond=lambda elem: elem[GroupIdentityAttachDetachTypeIdentifier].value == "attach"),
        Type1(GroupIdentityDetachmentDownlink, cond=lambda elem: elem[GroupIdentityAttachDetachTypeIdentifier].value == "detach"),
        Type1(GroupIdentityAddressType),
        Type1(Gssi, cond=lambda elem: elem[GroupIdentityAddressType].value in ["GSSI", "GTSI", "GTSI+(V)GSSI"]),
        Type1(AddressExtension, cond=lambda elem: elem[GroupIdentityAddressType].value in ["GTSI", "GTSI+(V)GSSI"]),
        Type1(VGssi, cond=lambda elem: elem[GroupIdentityAddressType].value in ["(V)GSSI", "GTSI+(V)GSSI"]),
    ]
    type2 = []
    type34 = []


class GroupIdentityLocationAccept(CompoundElement):
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


class DefaultGroupAttachementLifetime(IntElement):
    name = "Default group attachment lifetime"
    identifier = 1
    length = 2


class AuthenticationDownlink(IntElement):
    name = "Authentication Downlink"
    identifier = 10
    length = None  # TODO


class Proprietary(IntElement):
    name = "Proprietary"
    identifier = 15
    length = None  # TODO
