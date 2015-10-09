from pytetra.pdu.sublayer32pdu import LeafElement, CompoundElement, Type1, Type2, Type3


class CallIdentifier(LeafElement):
    name = "Call identifier"
    length = 14


class CallTimeout(LeafElement):
    name = "Call timeout"
    length = 4


class HookMethodSelection(LeafElement):
    name = "Hook method selection"
    length = 1


class SimplexDuplex(LeafElement):
    name = "Simplex/Duplex"
    length = 1


class TxGrant(LeafElement):
    name = "Tx grant"
    length = 2


class TxReqPerm(LeafElement):
    name = "Tx req perm"
    length = 1


class CallOwnership(LeafElement):
    name = "Call ownership"
    length = 1


class CallPriority(LeafElement):
    name = "Call priority"
    length = 4


class CircuitModeType(LeafElement):
    name = "Circuit mode type"
    length = 3


class EncryptionFlag(LeafElement):
    name = "Encryption flag"
    length = 1


class CommunicationType(LeafElement):
    name = "Communication type"
    length = 2


class SlotsPerFrame(LeafElement):
    name = "Slots per frame"
    length = 2


class SpeechService(LeafElement):
    name = "Speech service"
    length = 2


class BasicServiceInfos(CompoundElement):
    name = "Basic service infos"
    type1 = [
        Type1(CircuitModeType),
        Type1(EncryptionFlag),
        Type1(CommunicationType),
        Type1(SlotsPerFrame),
        Type1(SpeechService),
    ]
    type2 = []
    type34 = []


class TemporaryAddress(LeafElement):
    name = "Temporary address"
    length = 24


class NotificationIndicator(LeafElement):
    name = "Notification indicator"
    length = 6


class Facility(LeafElement):
    name = "Facility"
    length = None


class Proprietary(LeafElement):
    name = "Proprietary"
    length = None


class CallingPartyTypeIdentifier(LeafElement):
    name = "Calling party type identifier"
    length = 2


class CallingPartyAddressSsi(LeafElement):
    name = "Calling party address SSI"
    length = 24


class CallingPartyExtension(LeafElement):
    name = "Calling party extension"
    length = 24


class ExternalSubscriberNumber(LeafElement):
    name = "External subscriber number"
    length = None


class DmMsAddress(LeafElement):
    name = "DM-MS address"
    length = None


class DisconnectCause(LeafElement):
    name = "Disconnect cause"
    length = 5
