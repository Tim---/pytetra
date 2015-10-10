from pytetra.pdu.sublayer32pdu import IntElement, EnumElement, CompoundElement, Type1, Type2, Type3


class PduType(IntElement):
    name = "PDU Type"
    length = 5


class CallIdentifier(IntElement):
    name = "Call identifier"
    length = 14


class CallTimeout(IntElement):
    name = "Call timeout"
    length = 4


class HookMethodSelection(IntElement):
    name = "Hook method selection"
    length = 1


class SimplexDuplexSelection(IntElement):
    name = "Simplex/duplex selection"
    length = 1


class TxGrant(IntElement):
    name = "Tx grant"
    length = 2


class TxReqPerm(IntElement):
    name = "Tx req perm"
    length = 1


class CallOwnership(IntElement):
    name = "Call ownership"
    length = 1


class CallPriority(IntElement):
    name = "Call priority"
    length = 4


class CircuitModeType(IntElement):
    name = "Circuit mode type"
    length = 3


class EncryptionFlag(IntElement):
    name = "Encryption flag"
    length = 1


class CommunicationType(IntElement):
    name = "Communication type"
    length = 2


class SlotsPerFrame(IntElement):
    name = "Slots per frame"
    length = 2


class SpeechService(IntElement):
    name = "Speech service"
    length = 2


class BasicServiceInformation(CompoundElement):
    name = "Basic service information"
    type1 = [
        Type1(CircuitModeType),
        Type1(EncryptionFlag),
        Type1(CommunicationType),
        Type1(SlotsPerFrame),
        Type1(SpeechService),
    ]
    type2 = []
    type34 = []


class TemporaryAddress(IntElement):
    name = "Temporary address"
    length = 24


class NotificationIndicator(IntElement):
    name = "Notification indicator"
    length = 6


class Facility(IntElement):
    name = "Facility"
    length = None


class Proprietary(IntElement):
    name = "Proprietary"
    length = None


class CallingPartyTypeIdentifier(IntElement):
    name = "Calling party type identifier"
    length = 2


class CallingPartyAddressSsi(IntElement):
    name = "Calling party address SSI"
    length = 24


class CallingPartyExtension(IntElement):
    name = "Calling party extension"
    length = 24


class ExternalSubscriberNumber(IntElement):
    name = "External subscriber number"
    length = None


class DmMsAddress(IntElement):
    name = "DM-MS address"
    length = None


class DisconnectCause(IntElement):
    name = "Disconnect cause"
    length = 5


class CallTimeoutSetUpPhase(IntElement):
    name = "Call time-out, set-up phase"
    length = 3


class CallStatus(IntElement):
    name = "Call status"
    length = 3
